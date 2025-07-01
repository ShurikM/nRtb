* connect to DB docker `docker exec -it rtb-postgres psql -U rtb_user -d rtb`
* start the docker `docker-compose up --build`
* rebuild the protos `python -m grpc_tools.protoc -I=./shared/protos --python_out=./shared/protos --grpc_python_out=./shared/protos ./shared/protos/events.proto`
* start the grpc server ` python rtb_client_backend/app/grpc_server.py`
* start the rest api backend `poetry run uvicorn app.main:app --reload`
* start the frontend `npm run dev`
* 
`



