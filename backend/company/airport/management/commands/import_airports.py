from datetime import datetime
import json
import numpy as np
import pandas as pd
import requests
from rest_framework.response import Response
from django.core.management.base import BaseCommand
from airport.models import Airport

class Command(BaseCommand):
    
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.domestic_airport = []
        self.log = {
            "model": "Airport",
            "started_at": datetime.utcnow(),
            "finished_at": None,
            "success": False,
            "n_records_inserted": 0,
            "details": None
        }

    def handle(self, *args, **options):
        print("[ *** 1. QUERYING THE DOMESTIC AIRPORTS API *** ]")
        self.get_api_data()
        
        print("[ *** 2. COMPARING API DATA WITH DATABASE *** ]")
        self.segregate_data_for_action()
        
        print("[ *** 3. LOADING NEW DATA *** ]")
        if not self.domestic_airport.empty:
            log_insercao = self.load_data()
            if log_insercao.get("error"):
                self.log["details"] = log_insercao["details"]
                return self.log
            self.log["n_records_inserted"] = log_insercao["inserted"]
        
        print("[ *** 4. UPDATING EXISTING DATA *** ]")
        if not self.data_to_update.empty:
            log_updated = self.update_data(
            updated_columns=['iata','city', 'lat', 'lon', 'state'])
            if log_updated.get("error"):
                self.log["details"] = log_updated["details"]
                return self.log             
            self.log["n_records_updated"] = log_updated["updated"]
        self.log["success"] = True
        self.log["finished_at"] = datetime.utcnow()
        return str(self.log)
    
    def get_api_data(self):
        try: 
            request = requests.get(
                url="http://stub.2xt.com.br/air/airports/pzrvlDwoCwlzrWJmOzviqvOWtm4dkvuc",
                auth=("demo","swnvlD")
            )
            response_data = json.loads(request.content)
            domestic_airport_data = [response_data[key] for key in response_data]
            self.domestic_airport = pd.DataFrame(domestic_airport_data)
            
        except Exception as err:
            self.log["details"] = str(err)
            return 
        
    def load_data(self):
        result = {}
        batch_size = 500
        objs = (
            self.domestic_airport
            .replace({np.nan: None})
            .to_dict('records'))

        ins_list = [Airport(**vals) for vals in objs]
        try:
            Airport.objects.bulk_create(ins_list, batch_size)
            result['inserted'] = len(objs)
        except Exception as err:
            result['error'] = True
            result["details"] = f'Failed to insert data at Airport Model: {str(err)}'
        return result
            
    def segregate_data_for_action(self) -> pd.DataFrame:
        """Compares the inputed dataframe data to the existing data on the recipient model"""
        df = pd.merge(
            self.domestic_airport, self.existing_data,
            how = 'left', on = 'iata',
            suffixes=['', '_db'])
        columns = [col for col in df.columns if not col.endswith('_db')]
        self.domestic_airport = (
            df.loc[df['id'].isna(), columns]
            .drop(columns=["id"])
            .reset_index(drop=True)
        )

        self.data_to_update = (
            df.loc[df['id'].notna(), :]
            .pipe(self.filter_changed_values))
        
    def update_data(self, updated_columns):
        result = {}
        batch_size = 500
        objs = (
            self.data_to_update
            .replace({np.nan: None})
            .to_dict('records'))
        items = [Airport(**vals) for vals in objs]
        try:
            Airport.objects.bulk_update(
                items, updated_columns, batch_size)
            result['updated'] = len(objs)
        except Exception as err:
            result['error'] = True
            result["details"] = f'Failed to update airports data: {str(err)}'
        return result
    
    def filter_changed_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """This methods returns only the data that is new in comparision to the existing data"""
        if df.empty:
            return pd.DataFrame()
       
        for col in [c for c in df.columns if c.endswith('_db')]:
            new_values = df[col.replace("_db", "")]
            
            db_values = df[col]
            
            df[col + "_test"] = np.where(
                (new_values.notna()) & (new_values != db_values), True, False
            )
        
        has_new_data = (
            df[[c for c in df.columns if c.endswith("_test")]].any(axis=1))
        
        return (
            df.loc[has_new_data, [c for c in df.columns if not c.endswith(('_db', '_test'))]]
            .reset_index(drop=True))
    
        
    @property
    def existing_data(self) -> None:
        columns = ['id' , 'iata','city', 'lat', 'lon', 'state']
        qs = Airport.objects.values_list(*columns)
        df = pd.DataFrame(list(qs), columns=columns)
        float_columns = ['lat', 'lon']
        for col in float_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype('float', errors='ignore')
        
        return df
    
   
