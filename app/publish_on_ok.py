import hashlib
import json

import requests


def get_hash_signature(signature):
    return hashlib.md5(signature.encode('utf-8')).hexdigest()


def get_upload_url(app_key, token, session_key, group_id):
    ''' Готовим URL сервера ok для загрузки'''
    signature = f'application_key={app_key}format=jsongid={group_id}method=photosV2.getUploadUrl{session_key}'
    sig = get_hash_signature(signature)
    params = {
        'application_key': app_key,
        'format': 'json',
        'gid': group_id,
        'method': 'photosV2.getUploadUrl',
        'sig': sig,
        'access_token': token,
    }
    ok_url = 'https://api.ok.ru/fb.do'
    response = requests.get(ok_url, params=params)
    response.raise_for_status()
    return response.json()['upload_url']


def upload_photo_ok(url, img_filename):
    ''' Загружаем картинку на сервер ok '''

    with open(img_filename, 'rb') as file:
        ok_file = {
            'filename': file,
        }
        response = requests.post(url, files=ok_file)
    response.raise_for_status()
    response_params = response.json()
    for key in response_params['photos']:
        photo_token = response_params['photos'][key]['token']
        return photo_token


def publish_post_to_ok(app_key, token, session_key, group_id, text, photo_token=None):
    ''' Публикуем пост в сообществе в vk '''
    if not photo_token:
        attachment = {
            "media": [
                {
                    "type": "text",
                    "text": text
                }
            ]
        }
    elif not text:
        attachment = {
            "media": [
                {
                    "type": "photo",
                    "list": [
                        {"id": photo_token}
                    ]
                }
            ]
        }
    else:
        attachment = {
            "media": [
                {
                    "type": "photo",
                    "list": [
                        {"id": photo_token}
                    ]
                },
                {
                    "type": "text",
                    "text": text
                }
            ]
        }
    attachment_json = json.dumps(attachment)
    signature = f'application_key={app_key}attachment={attachment}format=jsongid={group_id}method=mediatopic.posttype=GROUP_THEME{session_key}'
    sig = get_hash_signature(signature)
    params = {
        'application_key': app_key,
        'attachment': attachment_json,
        'format': 'json',
        'gid': group_id,
        'method': 'mediatopic.post',
        'type': 'GROUP_THEME',
        'sig': sig,
        'access_token': token,
    }
    ok_url = 'https://api.ok.ru/fb.do'
    response = requests.get(ok_url, params=params)
    response.raise_for_status()
    return response.json()


def delete_ok_post(app_key, token, session_key, topic_id):
    ''' Удаляем пост со стены '''

    signature = f'application_key={app_key}format=jsonmethod=mediatopic.deleteTopictopic_id={topic_id}{session_key}'
    sig = get_hash_signature(signature)
    params = {
        'application_key': app_key,
        'format': 'json',
        'method': 'mediatopic.deleteTopic',
        'topic_id': topic_id,
        'sig': sig,
        'access_token': token,
    }
    ok_url = 'https://api.ok.ru/fb.do'
    response = requests.get(ok_url, params=params)
    response.raise_for_status()
    return response.json()


def publish_to_ok(app_key, token, session_key, group_id, text=None, img_filename=None):
    ''' Собираем все вместе и выводим идентификатор нового поста в ok '''

    if not img_filename:
        post_id = publish_post_to_ok(app_key, token, session_key, group_id, text)
    else:
        upload_url = get_upload_url(app_key, token, session_key, group_id)
        photo_token = upload_photo_ok(upload_url, img_filename)

        post_id = publish_post_to_ok(app_key, token, session_key, group_id, text, photo_token)
    return post_id
