import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
    'projectId': 'todo-user-project',
})

db = firestore.client()


def get_users():
    return db.collection('users').get()


def get_user(user_id):
    return db.collection('users').document(user_id).get()


def get_user_id(username):
    users = get_users()
    for user in users:
        if user.to_dict()['username'] == username:
            return user.id


def register_user(user_data):
    db.collection(u'users').document(f'{user_data.uid}').set(
        {'username': user_data.username, 'password': user_data.password}
    )


def create_todo(user_id, description):
    todos_collection_ref = db.collection(
        'users').document(user_id).collection('todos')

    todos_collection_ref.add({'description': description, 'done': False})


def read_todo(user_id):
    return db.collection('users').document(user_id).collection('todos').get()


def delete_todo(user_id, todo_id):
    todo_ref = get_todo_ref(user_id=user_id, todo_id=todo_id)
    todo_ref.delete()


def update_todo(user_id, todo_id, done):
    todo_done = not bool(done)
    todo_ref = get_todo_ref(user_id=user_id, todo_id=todo_id)
    todo_ref.update({'done': todo_done})


def get_todo_ref(user_id, todo_id):
    return db.document(f'users/{user_id}/todos/{todo_id}')
