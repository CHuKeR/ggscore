from src.worker import send_finished_matches_to_users, send_updated_matches_to_user
from src.worker import update_future_dota_matches

if __name__ == '__main__':
    update_matches = update_future_dota_matches()
    if len(update_matches) > 0:
        send_updated_matches_to_user(update_matches)
    send_finished_matches_to_users()
