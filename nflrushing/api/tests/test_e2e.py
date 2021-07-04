import pytest

from stats.types import NFLRushingStats
from stats.cqrs.commands import CreateStatsCmd
from stats.models import EventTypes

from django.urls import reverse

Test_Data = [
    {
        "Player": "Joe Banyard",
        "Team": "JAX",
        "Pos": "RB",
        "Att": 2,
        "Att/G": 2,
        "Yds": 7,
        "Avg": 3.5,
        "Yds/G": 7,
        "TD": 0,
        "Lng": "7",
        "1st": 0,
        "1st%": 0,
        "20+": 0,
        "40+": 0,
        "FUM": 0
    },
    {
        "Player": "Shaun Hill",
        "Team": "MIN",
        "Pos": "QB",
        "Att": 5,
        "Att/G": 1.7,
        "Yds": 5,
        "Avg": 1,
        "Yds/G": 1.7,
        "TD": 1,
        "Lng": "9",
        "1st": 0,
        "1st%": 0,
        "20+": 0,
        "40+": 0,
        "FUM": 0
    },
]


@pytest.mark.django_db
def test_view(client):
    url = reverse('list-stats')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_view_data(client):
    url = reverse('list-stats')
    for item in Test_Data:
        stats_entry = NFLRushingStats(json=item)
        CreateStatsCmd().execute(stats_entry, EventTypes.CREATE_SYSTEM)

    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data['data']) == 2
    assert response.data['data'][0]['Player'] == Test_Data[0]["Player"] or response.data['data'][1]['Player'] == Test_Data[0]["Player"]
    assert response.data['data'][0]['Player'] == Test_Data[1]["Player"] or response.data['data'][1]['Player'] == Test_Data[1]["Player"]


@pytest.mark.django_db
def test_view_data_paging(client):
    url = reverse('list-stats')
    for item in Test_Data:
        stats_entry = NFLRushingStats(json=item)
        CreateStatsCmd().execute(stats_entry, EventTypes.CREATE_SYSTEM)

    data = {'page': 1, "page_size": 1}

    response = client.get(url, data)
    assert response.status_code == 200
    assert len(response.data['data']) == 1
    assert response.data['data'][0]['Player'] == Test_Data[0]["Player"] or response.data['data'][0]['Player'] == Test_Data[1]["Player"]

    data2 = {'page': 2, "page_size": 1}

    response2 = client.get(url, data2)
    assert response2.status_code == 200
    assert len(response2.data['data']) == 1
    assert response.data['data'][0]['Player'] == Test_Data[0]["Player"] or response.data['data'][0]['Player'] == Test_Data[1]["Player"]

    assert response2.data['data'][0]['Player'] is not response.data['data'][0]['Player']


@pytest.mark.django_db
def test_view_data_filtered(client):
    url = reverse('list-stats')
    for item in Test_Data:
        stats_entry = NFLRushingStats(json=item)
        CreateStatsCmd().execute(stats_entry, EventTypes.CREATE_SYSTEM)

    data = {'filter': 'Shaun'}

    response = client.get(url, data)
    assert response.status_code == 200
    assert len(response.data['data']) == 1
    assert response.data['data'][0]['Player'] == 'Shaun Hill'


@pytest.mark.django_db
def test_view_data_sorted_Lng(client):
    url = reverse('list-stats')
    for item in Test_Data:
        stats_entry = NFLRushingStats(json=item)
        CreateStatsCmd().execute(stats_entry, EventTypes.CREATE_SYSTEM)

    data = {'sort': 'LONGEST_RUSH', 'sort_by': "ASC"}

    response = client.get(url, data)
    assert response.status_code == 200
    assert int(response.data['data'][0]['Lng']) <= int(
        response.data['data'][1]['Lng'])

    data2 = {'sort': 'LONGEST_RUSH', 'sort_by': "DESC"}

    response2 = client.get(url, data2)
    assert response2.status_code == 200
    assert int(response2.data['data'][0]['Lng']
               ) >= int(response2.data['data'][1]['Lng'])


@pytest.mark.django_db
def test_view_data_sorted_TD(client):
    url = reverse('list-stats')
    for item in Test_Data:
        stats_entry = NFLRushingStats(json=item)
        CreateStatsCmd().execute(stats_entry, EventTypes.CREATE_SYSTEM)

    data = {'sort': 'TOTAL_RUSHING_TOUCHDOWN', 'sort_by': "ASC"}

    response = client.get(url, data)
    assert response.status_code == 200
    assert int(response.data['data'][0]['TD']) <= int(
        response.data['data'][1]['TD'])

    data2 = {'sort': 'TOTAL_RUSHING_TOUCHDOWN', 'sort_by': "DESC"}

    response2 = client.get(url, data2)
    assert response2.status_code == 200
    assert int(response2.data['data'][0]['TD']
               ) >= int(response2.data['data'][1]['TD'])


@pytest.mark.django_db
def test_view_data_sorted_Yds(client):
    url = reverse('list-stats')
    for item in Test_Data:
        stats_entry = NFLRushingStats(json=item)
        CreateStatsCmd().execute(stats_entry, EventTypes.CREATE_SYSTEM)

    data = {'sort': 'TOTAL_RUSHING_YARDS', 'sort_by': "ASC"}

    response = client.get(url, data)
    assert response.status_code == 200
    assert int(response.data['data'][0]['Yds']) <= int(
        response.data['data'][1]['Yds'])

    data2 = {'sort': 'TOTAL_RUSHING_YARDS', 'sort_by': "DESC"}

    response2 = client.get(url, data2)
    assert response2.status_code == 200
    assert int(response2.data['data'][0]['Yds']
               ) >= int(response2.data['data'][1]['Yds'])
