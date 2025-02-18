import pandas as pd
from datetime import date, timedelta
from sales import Sales
from inventory import Inventory
from sftp import SFTPServerClient
from decouple import config


from pathlib import Path
from helper import log

today = date.today()  # - timedelta(days=1)


def get_sales():
    log("Initiating Get Sales Function")
    my_file = Path(f"output/Sales {today}.csv")
    if my_file.exists():
        log("File Exists in the local Directory")
        print("File Exists in the local directory")
        return True
    try:
        # dataframe from list of dicts
        df = pd.DataFrame.from_dict(Sales.get_sales_per_store()).set_index('channel')
        df = df.rename(columns={"channel": "Channel", "storeId": ";Store ID", "itemLookupCode": "Item",
                                "size": "Size", "color": "Color", "isGrandTotalRowTotal": "IsGrandTotalRowTotal",
                                "dateSold": "Date_Sold", "sumQtySold": "SumQty_Sold", "sumRevenue": "SumRevenue",
                                "discountValue": "Discount_Value", "itemStatus": "ItemStatus",
                                "styleColor": "Style&Color"})
        df['Size'] = df['Size'].astype(str)

        df.to_csv(f"output/Sales {today}.csv")
    except:
        log("Error While Creating DataFrame")
        print("Error While Creating DataFrame")
        return False
    else:
        log("Sales File Generated Successfully")
        return True


def get_inventory():
    log("Initiating Get Inventory Function")
    my_file = Path(f"output/Store Inventory {today}.csv")
    if my_file.exists():
        log("File Exists in the local Directory")
        print("File Exists in the local directory")
        return True
    try:
        df = pd.DataFrame.from_dict(Inventory.get_inventory_per_store()).set_index('channel')
        df = df.rename(columns={"channel": "Channel", "storeId": ";Store ID", "storeName": "Store_Name",
                                "itemLookupCode": "ItemLookupCode",
                                "styleColor": "Style&Color", "lastCheckDate": "Today_Date_OH",
                                "mostRecentQtyUpdate": "MostRecentQtyUpdate",
                                "itemStatus": "ItemStatus", "isGrandTotalRowTotal": "IsGrandTotalRowTotal",
                                "qtyOnHand": "SumQty_OH"})
        df.to_csv(f"output/Store Inventory {today}.csv")
    except:
        log("Error While Creating DataFrame")
        print("Error While Creating DataFrame")
        return False
    else:
        log("Inventory File Generated Successfully")
        return True


def send_to_ftp(file_name, remote_path):
    log("Initiating FTP Send Function")
    sftp_client = SFTPServerClient(hostname=config('SFTP_HOST'), port=config('SFTP_PORT'),
                                   username=config('SFTP_USERNAME'),
                                   password=config('SFTP_PASSWORD'))
    sftp_client.connect()

    files_list = sftp_client.getListofFiles(remoteFilePath=remote_path)
    if file_name in files_list:
        log(f"File {file_name} Already Exist in FTP")
        print("File Already Exist in FTP")
        status = False
    else:
        local_path = f"output/{file_name}"
        sftp_client.uploadFiles(remoteFilePath=f"{remote_path}/{file_name}", localFilePath=local_path)
        log(f"File {file_name} Uploaded Successfully to FTP")
        print("File Uploaded Successfully")
        status = True

    sftp_client.disconnect()
    return status


def main():
    if get_sales():
        send_to_ftp(remote_path=config('SALES_FTP_PATH'), file_name=f'Sales {today}.csv')
    if get_inventory():
        send_to_ftp(remote_path=config('INV_FTP_PATH'), file_name=f'Store Inventory {today}.csv')
    log("Execution Completed")
    log("---------------------")


if __name__ == "__main__":
    main()
