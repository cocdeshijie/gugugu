from app import create_app, db

app = create_app('default')


app.run(host='0.0.0.0', port=5000)

