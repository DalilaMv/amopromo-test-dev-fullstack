import React, { useEffect, useState } from 'react';
import { Breadcrumb, Layout, Menu, Table, Switch, Modal, Input, message, Button, Tooltip, Row, Col, Select} from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { connect, Dispatch, Loading } from 'umi';
import type { IAirportsState, IAirports } from './model';
import { SearchOutlined } from '@ant-design/icons';
import enUS from 'antd/lib/locale-provider/en_US';

interface DataProps {
  loading: boolean;
  airports: IAirportsState;
  dispatch: Dispatch;
}

const AirportsPage = (props: DataProps) => {
  const { dispatch } = props;
  const { Header, Content, Footer } = Layout;
  const [airports, changeAirports] = useState<Record<string, any>[]>([]);
  const [reasonModalIsOpen, setReasonModalIsOpen] = useState(false);
  const [status, setStatus] = useState(undefined);
  const reason = React.useRef(null);
  const selected_id =  React.useRef(null);
  const selected_is_active = React.useRef(null);
 
  const { TextArea } = Input;

  useEffect(() => {
    dispatch({ type: 'airports/init' });
  }, []);

  useEffect(() => {
    changeAirports(props.airports.airports);
  }, [props.airports.airports]);

  async function handleSwitchChange(value: any, record: any) {
    selected_id.current = record.id;
    selected_is_active.current = value
    reason.current = null
    if (!value) {
      showModal()
    } else {
      changeAirportStatus('activate')
    }
  }

  const showModal = () => {
    setReasonModalIsOpen(true);
  };

  const hideModal = () => {
    reason.current = null
    setReasonModalIsOpen(false);
  };

  const handleOkClick = () => {
    changeAirportStatus('deactivate')
  }

  function changeAirportStatus(operation_type: any) {
    dispatch({
      type: 'airports/editAirportStatus',
      payload: {
        id: selected_id.current,
        is_active: selected_is_active.current,
        inactive_reason: reason.current,
      }
    }).then(() => {
      message.success({
        type: 'success',
        content: `${operation_type === 'activate' ? 'Airport activated' :'Airport disabled successfully.' }`,
        duration: 10,
      });
      hideModal()
    })
  }

  interface DataType {
    id: number;
    key: number;
    iata: string;
    city: string;
    lat: number;
    lon: number;
    state: string;
    is_active: Boolean;
    inactive_reason: string;
  }

  const columns: ColumnsType<DataType> = [
    {
      title: 'IATA',
      dataIndex: 'iata',
      align: 'center',
    },
    {
      title: 'City',
      dataIndex: 'city',
      align: 'center',
    },
    {
      title: 'State',
      dataIndex: 'state',
      align: 'center',
    },
    {
      title: 'Latitude',
      dataIndex: 'lat',
      align: 'center',
    },
    {
      title: 'Longitude',
      dataIndex: 'lon',
      align: 'center',
    },
    {
      title: 'Status',
      dataIndex: 'is_active',
      align: 'center',
      render: (value: boolean, record: any) => {
        return (
          <Switch 
            defaultChecked={value} 
            onChange={(e) => handleSwitchChange(e, record)}
            checkedChildren="ative" 
            unCheckedChildren="inactive"
          />
        )
      }
    },
    {
      title: 'Details',
      dataIndex: 'inactive_reason',
      align: 'center',
      render: (value: string, record: any) => {
        return (
          <Tooltip title={value}>
            <Button 
              shape='circle'
              icon={<SearchOutlined />}
              disabled={record.is_active}
            />
          </Tooltip>
        )
      }
    }
  ];

  const data: DataType[] = [];
  
  const options = [
    { key: 1, name: 'active', value: true},
    { key: 2, name: 'inactive', value: false}
  ]
  return (
    <>
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ position: 'sticky', top: 0, zIndex: 1, width: '100%' }}>
        <div
          style={{
            float: 'left',
            width: 120,
            height: 31,
            margin: '16px 24px 16px 0',
            background: 'rgba(255, 255, 255, 0.2)',
          }}
        />
        <Menu
          theme="dark"
          mode="horizontal"
          defaultSelectedKeys={['2']}
          items={[{
            key: "1",
            label: "Airports"
          }]}
        />
      </Header>
      <Content className="site-layout" style={{ padding: '0 50px' }}>
        <Breadcrumb style={{ margin: '16px 0' }}>
          <Breadcrumb.Item>Home</Breadcrumb.Item>
          <Breadcrumb.Item>Airports</Breadcrumb.Item>
        </Breadcrumb>
        <div style={{ padding: 24, minHeight: 500, background: "white" }}>
          <Row justify={"end"}>
            {/* <Col span={3}> */}
            <Select
              allowClear
              placeholder="Filter by active/inactive"
              style={{ width: '240px', paddingBottom: '7px' }}
              loading={props.loading}
              disabled={props.loading}
              value={status}
              onChange={(value: any) => setStatus(value)}
            >
              {options.map((i) => (
                <Select.Option value={i.value} key={i.key}>
                  {i.name}
                </Select.Option>
              ))}
            </Select>
            {/* </Col> */}
          </Row>
          <Table 

            rowKey={"key"}
            loading={props.loading}
            columns={columns} 
            dataSource={airports.filter((element: any) => 
              status !== undefined ? element.is_active === status : true)
            } 
            pagination={{ 
              pageSizeOptions: ['5', '10', '30', '100', '500'],
              defaultPageSize: 5,
            }}
            
            scroll={{ y: 'max-content' }} 
          />
        </div>

      </Content>
      <Footer style={{ textAlign: 'center' }}>Test Dev Full Stack ©2022 Created by Dalila Mylena Vieira</Footer>
    </Layout>
    <Modal
      destroyOnClose
      title=""
      open={reasonModalIsOpen}
      onOk={handleOkClick}
      onCancel={hideModal}
      okText="Deactivate"
      cancelText="Cancel"
    >
      <p>Please advise why this airport is being shut down:</p>
      <TextArea  onChange={(e: any) => reason.current = e.target.value} rows={4} />
    </Modal>
    </>
  );
};

interface IConnect {
  airports: IAirportsState;
  loading: Loading;
}

export default connect(({ airports, loading }: IConnect) => ({
  airports,
  loading: loading.models.airports,
}))(AirportsPage);
