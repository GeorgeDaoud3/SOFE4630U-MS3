import redis        # pip install redis
import io;

ip=""
r = redis.Redis(host=ip, port=6379, db=0,password='SOFE4630U')

value=r.get('OntarioTech');

with open("./recieved.jpg", "wb") as f:
    f.write(value);
