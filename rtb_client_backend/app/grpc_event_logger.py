from concurrent import futures
import grpc
from shared.protos import events_pb2, events_pb2_grpc
from shared.database import SessionLocal
from sqlalchemy import insert
import logging

class EventLogger(events_pb2_grpc.EventLoggerServicer):
    def LogBidRequest(self, request, context):
        db = SessionLocal()
        stmt = insert(db.tables['bid_requests']).values(
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
            floor_price=request.floor_price
        )
        db.execute(stmt)
        db.commit()
        db.close()
        return events_pb2.LogAck(success=True)

    def LogBid(self, request, context):
        db = SessionLocal()
        stmt = insert(db.tables['bids']).values(
            bid_request_id=request.bid_request_id,
            campaign_id=request.campaign_id,
            creative_id=request.creative_id,
            bid_price=request.bid_price,
            won=request.won,
            win_price=request.win_price
        )
        db.execute(stmt)
        db.commit()
        db.close()
        return events_pb2.LogAck(success=True)

    def LogImpression(self, request, context):
        db = SessionLocal()
        stmt = insert(db.tables['impressions']).values(
            bid_id=request.bid_id,
            campaign_id=request.campaign_id,
            creative_id=request.creative_id,
            cost=request.cost
        )
        db.execute(stmt)
        db.commit()
        db.close()
        return events_pb2.LogAck(success=True)

    def LogClick(self, request, context):
        db = SessionLocal()
        stmt = insert(db.tables['clicks']).values(
            impression_id=request.impression_id,
            campaign_id=request.campaign_id,
            creative_id=request.creative_id
        )
        db.execute(stmt)
        db.commit()
        db.close()
        return events_pb2.LogAck(success=True)
