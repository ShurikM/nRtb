import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

import grpc
from concurrent import futures
from shared.database import SessionLocal
from shared import models
from datetime import datetime
from shared.protos import events_pb2, events_pb2_grpc



class EventLoggerServicer(events_pb2_grpc.EventLoggerServicer):
    def LogBidRequest(self, request, context):
        db = SessionLocal()
        try:
            bid_request = models.BidRequest(
                request_id=request.request_id,
                imp_id=request.imp_id,
                auction_id=request.auction_id,
                site_domain=request.site_domain,
                site_page=request.site_page,
                user_country=request.user_country,
                user_language=request.user_language,
                device_type=request.device_type,
                banner_width=request.banner_width,
                banner_height=request.banner_height,
                floor_price=request.floor_price,
                timestamp=datetime.utcnow(),
            )
            db.add(bid_request)
            db.commit()
            return events_pb2.LogAck(success=True)
        except Exception as e:
            db.rollback()
            return events_pb2.LogAck(success=False)
        finally:
            db.close()

    def LogBid(self, request, context):
        db = SessionLocal()
        try:
            bid = models.Bid(
                bid_request_id=request.bid_request_id,
                campaign_id=request.campaign_id,
                creative_id=request.creative_id,
                bid_price=request.bid_price,
                won=request.won,
                win_price=request.win_price,
                timestamp=datetime.utcnow(),
            )
            db.add(bid)
            db.commit()
            return events_pb2.LogAck(success=True)
        except Exception:
            db.rollback()
            return events_pb2.LogAck(success=False)
        finally:
            db.close()

    def LogImpression(self, request, context):
        db = SessionLocal()
        try:
            impression = models.Impression(
                bid_id=request.bid_id,
                campaign_id=request.campaign_id,
                creative_id=request.creative_id,
                cost=request.cost,
                timestamp=datetime.utcnow(),
            )
            db.add(impression)
            db.commit()
            return events_pb2.LogAck(success=True)
        except Exception:
            db.rollback()
            return events_pb2.LogAck(success=False)
        finally:
            db.close()

    def LogClick(self, request, context):
        db = SessionLocal()
        try:
            click = models.Click(
                impression_id=request.impression_id,
                campaign_id=request.campaign_id,
                creative_id=request.creative_id,
                timestamp=datetime.utcnow(),
            )
            db.add(click)
            db.commit()
            return events_pb2.LogAck(success=True)
        except Exception:
            db.rollback()
            return events_pb2.LogAck(success=False)
        finally:
            db.close()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    events_pb2_grpc.add_EventLoggerServicer_to_server(EventLoggerServicer(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
