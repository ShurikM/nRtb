import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import grpc
from shared.protos import events_pb2, events_pb2_grpc

def test_log_bid_request():
    channel = grpc.insecure_channel("localhost:50052")
    stub = events_pb2_grpc.EventLoggerStub(channel)

    request = events_pb2.BidRequestLog(
        request_id="req_001",
        imp_id="imp_001",
        auction_id="auc_001",
        site_domain="test.com",
        site_page="https://test.com/page",
        user_country="US",
        user_language="en",
        device_type="desktop",
        banner_width=300,
        banner_height=250,
        floor_price=0.25
    )

    response = stub.LogBidRequest(request)
    print("LogBidRequest success:", response.success)


if __name__ == "__main__":
    test_log_bid_request()
