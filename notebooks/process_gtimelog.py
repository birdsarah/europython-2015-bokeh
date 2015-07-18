import datetime
import pandas as pd
import numpy as np

from bokeh.models import ColumnDataSource


def get_work_df():
    """
    Takes a gtimelog DataFrame, and removes the non-work categories
    """
    gt_df = _get_raw_df()
    gt_df = gt_df[~gt_df.activity.str.contains(r'\*\*\*')]
    return gt_df


def get_processed_df():
    return add_processed_columns(get_work_df())


def get_today_df():
#    today = datetime.datetime(2015, 6, 22)
    today = datetime.datetime(2015, 7, 10)
    processed = add_processed_columns(get_work_df())
    return get_today(today, processed)


def get_bar_chart_df(today_df):
    categories = list(today_df.parent_activity.unique())

    parent_df = today_df[today_df.parent_activity == categories[0]]
    summed = parent_df.groupby('sub_activity').sum().sort('human', ascending=False)
    summed['from total'] = summed.human.sum() - summed.human

    return summed


def get_plotting_chart_df():
    processed = get_processed_df()
    today = datetime.datetime(2015, 7, 10)
    start = today - datetime.timedelta(days=2)  # Start the plot two days ago
    end = today

    df = processed[(processed.timestamp >= start) & (processed.timestamp <= end)]
    df = df[df.activity != 'start']
    df['activity_bottom'] = df.formatted_activity + ':0.1'
    df['activity_top'] = df.formatted_activity + ':0.9'
    # Note Cannot serialize time deltas so don't want in source
    data = df[['start', 'end', 'formatted_activity', 'activity_bottom', 'activity_top']]
    activities = list(data.formatted_activity.unique())
    return start, end, activities, data


def get_models_sources_and_activities():
    raw = get_processed_df()
    first_day = raw.loc[0, 'timestamp']
    last_day = datetime.datetime.today()

    parent_activities = list(raw.parent_activity.unique())
    parent_activities.remove('Start')

    start_df = raw[raw.activity == 'start']
    nan_df = start_df.copy()
    nan_df['delta'] = np.NaN
    nan_df['activity'] = '_'

    dfs = {}

    # Build a dictionary of frames - one for each category
    for parent_activity in parent_activities:
        activity_df = raw[raw.parent_activity == parent_activity]

        # Add in the start rows with 0 deltas and do cumsum
        activity_df = activity_df.append(start_df)
        activity_df.sort('timestamp', inplace=True)
        activity_df['cumsum'] = np.cumsum(activity_df.groupby(activity_df.timestamp.dt.date)['delta'])
        activity_df['cumsum_hrs'] = activity_df['cumsum'].dt.seconds / (60 * 60)

        # Add in the nan rows so bokeh can plobt
        activity_df = activity_df.append(nan_df)
        activity_df.sort(['timestamp', 'activity'], inplace=True)

        dfs[parent_activity] = ColumnDataSource(activity_df[['cumsum_hrs', 'timestamp']])

    return first_day, last_day, dfs, parent_activities


def _get_raw_df():
    raw = pd.read_table('timelog.txt', quotechar=' ', sep=': ', names=['timestamp', 'activity'], engine='python',)

    # Set the column types

    raw.timestamp = pd.to_datetime(raw.timestamp)
    raw = raw.drop_duplicates()

    ### Build the times
    raw['end'] = raw.timestamp
    raw['start'] = raw['end'].shift(1)

    raw['start'] = np.where(
        raw['activity'] == 'start',  # If the activity is start
        raw['timestamp'],  # Set the start to timestamp
        raw['start'],  # Else leave it as start
    )

    raw['delta'] = raw.end - raw.start

    return raw


def add_processed_columns(gt_df, general_activity_name='general'):
    """
    Takes a gtimelog DataFrame, and adds the following columns:
        * 'human' - the time delta in hours to 2 decimal places
        * 'parent_activity' - if the activity is 'Test data - sub category', parent is 'Test data'
        * 'sub_activity' - if the activity is 'Test data - sub category', sub is 'sub category'
    Also:
        * If the activity is the same as the parent activity,
          then sub_activity is set to general_activity_name
        * capitalizes the new activity columns
    """
    gt_df['human'] = gt_df.delta.dt.seconds / (60 * 60)
    gt_df.human = gt_df.human.round(2)

    gt_df['parent_activity'] = gt_df.activity.str.split(' - ').str[0]
    gt_df.parent_activity = gt_df.parent_activity.str.capitalize()

    gt_df['sub_activity'] = gt_df.activity.str.split(' - ').str[1]
    gt_df.sub_activity = np.where(
        gt_df.activity.str.lower() == gt_df.parent_activity.str.lower(),
        general_activity_name,
        gt_df.sub_activity
    )
    gt_df.sub_activity = gt_df.sub_activity.str.capitalize()

    gt_df['formatted_activity'] = gt_df.parent_activity + ' (' + gt_df.sub_activity + ')'

    return gt_df


def get_today(today, gt_df):
    """
    Returns today, with no start row in it
    """
    today_df = gt_df[gt_df.timestamp.dt.date == today.date()]
    today_df = today_df[today_df.activity != 'start']
    return today_df
