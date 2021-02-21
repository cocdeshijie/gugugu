from flask import request, jsonify,url_for
from . import api
import os
import secrets

api.root_path = './app/static/files'

@api.route('/test')
def test():
    return api.root_path

@api.route('/upload', methods=['GET', 'POST'])
def upload():
    #get posted file
    uploaded_file = request.files['file']
    #set file extension, name, mimetype and save to folder by mimetype
    file_extension = uploaded_file.filename.split('.')[-1]
    file_name = '.'.join([secrets.token_urlsafe(12), file_extension])
    mimetype = uploaded_file.mimetype
    save_target = os.path.join(api.root_path, mimetype.split('/')[0])
    os.makedirs(save_target, exist_ok=True)
    #other file just gets saved
    uploaded_file.save(os.path.join(save_target, file_name))
    return jsonify(
        code=200,
        url=request.host_url+url_for('static', filename='files/'+mimetype.split('/')[0]+'/'+file_name)
    )