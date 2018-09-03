from influxdb import InfluxDBClient
import json

"""

"""
class influx_writer():
    def __init__(self):
        user = 'admin'
        password = 'admin'
        host='localhost'
        port=8086
        self.dbname = 'perftool'
        dbuser = 'admin'
        dbuser_password = 'admin'
        self.client = InfluxDBClient(host, port, user, password, self.dbname)

    def create_datasource(self):
        try:
            # print("Create database: " + self.dbname)
            self.client.create_database(self.dbname)
        except Exception as e:
            # print(e)
        else:
            # print("In else")
        finally:
            # print("Datasource method is done with execution")
        

    def write_process_data(self,data):
        # print(data)
        json_body = [
            {
                "measurement": "process",
                "fields" : data
            }]
        # print(json_body)
        # print("Write points: {0}".format(json_body))
        self.client.write_points(json_body)

    def write_system_data(self,data):
        # print(data)
        json_body = [
            {
                "measurement": "system",
                "fields" : data
            }]
        # print(json_body)
        # print("Write points: {0}".format(json_body))
        self.client.write_points(json_body)

# def main(, port=8086):
    
#     query = 'select value from cpu_load_short;'
    # json_body = [
    #     {
    #         "measurement": "process",
    #         "tags": {
    #             "host": "server01",
    #             "region": "us-west"
    #         },
    #         "time": "2018-08-10T15:20:00Z",
    #         "fields": {
    #             "Float_value": 0.64,
    #             "Int_value": 3,
    #             "String_value": "Text",
    #             "Bool_value": True
    #         }
    #     }
    # ]



    

    

#     # print("Create a retention policy")
#     # client.create_retention_policy('awesome_policy', '3d', 3, default=True)

#     # print("Switch user: " + dbuser)
#     # client.switch_user(dbuser, dbuser_password)

    

#     print("Querying data: " + query)
#     result = client.query(query)

#     print("Result: {0}".format(result))

  

#     print("Drop database: " + dbname)
#     client.drop_database(dbname)



# if __name__ == '__main__':
#     args = parse_args()
#     main()
