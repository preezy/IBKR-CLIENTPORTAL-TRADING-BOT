from datetime import datetime
import websocket, json, ssl, sys

socket = "wss://localhost:5000/v1/api/ws"

# try:
#     import thread
# except ImportError:
#     import _thread as thread
# import time




minutes_processed = {}
minute_candlesticks = []
current_tick = None
previous_tick = None

def on_message(ws, message):
    global current_tick, previous_tick

    
    message_to_dict = json.loads(message)
    if 'args' in message_to_dict and message_to_dict['args']['authenticated']:
        ws.send('smd+107113386+{"fields":["31","83"]}')
    # print("=== Received Tick ===")
    # print(json.dumps(m, indent=4, sort_keys=True))
    # print(f"this is the type of m {type(m)}")
    if 'conid' in message_to_dict:
        previous_tick = current_tick
        current_tick = message_to_dict

        timestamp = current_tick['_updated']/1000
        date_time_object = datetime.fromtimestamp(timestamp)
        tick_dt = date_time_object.strftime("%m/%d/%Y %H:%M")
        current_last = current_tick['31']
        
        print("=== Received Tick ===")
        print(f"{tick_dt} @ {current_last}")

        if not tick_dt in minutes_processed:
            print("starting new candlestick")
            minutes_processed[tick_dt] = True
            print(minutes_processed)

            if len(minute_candlesticks) > 0:
                minute_candlesticks[-1]['close'] = previous_tick['31']
                if minute_candlesticks[-1]['close'] > minute_candlesticks[-1]['open']:
                    minute_candlesticks[-1]['bull'] = True
                else:
                    minute_candlesticks[-1]['bull'] = False

            minute_candlesticks.append({
                'minute': tick_dt,
                'last' : current_last,
                'open': current_last,
                'high': current_last,
                'low': current_last
            })

        if len(minute_candlesticks) > 0:
            current_candlestick = minute_candlesticks[-1]
            current_candlestick['last'] = current_last
            if current_last > current_candlestick['high']:
                current_candlestick['high'] = current_last
            if current_last < current_candlestick['low']:
                current_candlestick['low'] = current_last
            print("===Candlesticks===")
            for candlestick in minute_candlesticks:
                print(candlestick)
        
        # print("====this is previous tick====")
        # print(json.dumps(previous_tick, indent=4, sort_keys=True))
        # print("====this is current tick====")
        # print(json.dumps(current_tick, indent=4, sort_keys=True))


        # print(json.dumps(message_to_dict, indent=4, sort_keys=True))
    else:
        print("=== Recieved un solicited message ===")
        # print(json.dumps(message_to_dict, indent=4, sort_keys=True))


def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print("i'm in open")
    # def run(*args):
    #     for i in range(10000):
    #         time.sleep(1)
    #         ws.send('smd+265598+{"fields":["31","83"]}')
    #     time.sleep(1)
    #     ws.close()
    #     print("thread terminating...")
    # thread.start_new_thread(run, ())
    # ws.send('smd+383974339+{"fields":["31","83"]}')



if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(socket,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open

    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})