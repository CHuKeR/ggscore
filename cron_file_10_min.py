from src.worker import send_finished_matches_to_users, send_closest_matches_to_user
from src.worker import update_future_dota_matches, update_finished_dota_matches

if __name__ == '__main__':
    update_future_dota_matches()
    send_closest_matches_to_user()
    update_finished_dota_matches()
    send_finished_matches_to_users()
