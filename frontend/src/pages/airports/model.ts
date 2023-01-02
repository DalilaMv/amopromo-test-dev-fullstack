import type { Effect, Reducer } from 'umi';
import { getAirports, saveAirport } from './service';


export interface IAirports {
  id: number;
  key: number;
  iata: string;
  city: string;
  lat: number;
  lon: number;
  state: string;
  is_active: Boolean;
  inactive_reason: Boolean;
}

export interface IAirportsState {
  airports: IAirports[];
}

interface IAirportsModel {
  namespace: string;
  state: IAirportsState;
  effects: {
    init: Effect;
    fetchAirports: Effect;
    editAirportStatus: Effect;
  };
  reducers: {
    update: Reducer<IAirportsState>;
  };
}
const AirportsModel: IAirportsModel = {
  namespace: 'airports',

  state: {
    airports: [],
  },

  effects: {
    *init(_, { put }) {
      yield put({ type: 'fetchAirports' });
    },

    *fetchAirports({ payload }, { call, put }) {
      const response = yield call(getAirports, payload);
      yield put({
        type: 'update',
        payload: {
          airports: response?.map((item: any, index: number) => {
            return {
              ...item,
              key: index,
            };
          }),
        },
      });
    },

    *editAirportStatus({payload} , {call, put, select}) {
      const airports = yield select((state: any) => state.airports.airports);
      yield call(saveAirport, payload);

      for (let i = 0; i < airports.length; i += 1) {
        if (airports[i].id === payload.id) {
          airports[i].is_active = payload.is_active;
          airports[i].inactive_reason = payload.inactive_reason;
        }
      } 

      yield put({
        type: 'update',
        payload: {
          airports: [...airports],
        },
      });
    },
  
    
  },

  reducers: {
    update(state, { payload }) {
      return {
        ...state,
        ...payload,
      };
    },
  },
};
export default AirportsModel;
