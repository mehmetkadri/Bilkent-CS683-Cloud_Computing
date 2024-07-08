import json
import sys
import logging
import pymysql
import os

"""
The code creates the connection to your database outside of the handler function. 
Creating the connection in the initialization code allows the connection to be 
re-used by subsequent invocations of your function and improves performance. 
"""

# rds settings
user_name = os.environ['USER_NAME']
password = os.environ['PASSWORD']
rds_proxy_host = os.environ['RDS_PROXY_HOST']
db_name = os.environ['DB_NAME']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# create the database connection outside of the handler to allow connections to be
# re-used by subsequent function invocations.
try:
    conn = pymysql.connect(host=rds_proxy_host, user=user_name, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit(1)

logger.info("SUCCESS: Connection to RDS for MySQL instance succeeded")


def lambda_handler(event, context):

    print('event: ', event)
    # get info from event
    data = event['body-json']
    user_id = data['userid']
    login_info = data['loggedin']
    user_type = data['userType']
    add_amount = float(data['amount'])
    
    session = {
        'userid' : user_id,
        'loggedin' : login_info,
        'userType' : user_type
    }

    # some example SQL commands
    with conn.cursor() as cursor:

                if not('userid' in session and 'loggedin' in session):
            message = "Session info is not found."
            return {
                'statusCode': 400,  # Customizing the status code
                'body': {
                'message': message,  # Including custom message in the response body
                #'session_info': session_info
                }
            }
        
        query_balance ="""
        SELECT balance
        FROM Traveler
        WHERE Traveler.id = %s
        """
        cursor.execute(query_balance, (user_id,))
        previous_balance = float(cursor.fetchone()[0])
        
        new_balance = previous_balance + add_amount
        
        query_newbalance = """
        UPDATE Traveler 
        SET balance = %s
        WHERE Traveler.id = %s
        """
        cursor.execute(query_newbalance, (new_balance, user_id))
        
        message = "Deneme üç dört :)"
        logger.info(message)
    
    conn.commit()

    return {
        'statusCode': 200,  # Customizing the status code
        'body': json.dumps({
            'message': message  # Including custom message in the response body
        })
    }
