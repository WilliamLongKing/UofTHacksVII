import psycopg2
try:
    print "trying"
    conn = psycopg2.connect(database="songs", user = "postgres", password = "test", host = "35.225.65.195")
    print "success"
except:
    print "failed"