from airflow import DAG
import pendulum
from datetime import datetime,timedelta
from api.video_stats import get_playlist_id, get_video_ids, extract_video_data, save_to_json     

# local_tz = pendulum.timezone("Asia/Bangkok")
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    
    'email_on_failure': False,
    'email_on_retry': False,
    'email': "magic46c@gmail.com",
    # 'retries': 1,
    # 'retry_delay': timedelta(minutes=5),
    'max_active_runs': 1,
    'dagrun_timeout': timedelta(minutes=60),
    # 'start_date': datetime(2026, 1, 31, tzinfo=local_tz),  
     'start_date': pendulum.datetime(2026, 1, 30, tz="Asia/Bangkok"),
}

with DAG(
    dag_id ='produce_json',
    default_args=default_args,
    description='A simple DAG to produce JSON file from YouTube API',
    schedule="0 16 * * *",  # At 16:00 (6 PM) every day
    catchup=False,
) as dag:
    
    # Define the tasks
    playlist_id = get_playlist_id()
    video_ids = get_video_ids(playlist_id)
    extract_data = extract_video_data(video_ids)
    save_to_json_task = save_to_json(extract_data)

    # Define task dependencies
    playlist_id >> video_ids >> extract_data >> save_to_json_task