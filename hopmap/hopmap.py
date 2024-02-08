import click
import subprocess
from scapy.all import *
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import requests


@click.command()
@click.option('--host', default='102.128.168.1')
def plot(host):
  locations = traceroute(host)
  draw_map_with_arrows(locations)

def draw_map_with_arrows(locations):
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_global()
    ax.add_feature(cfeature.LAND, facecolor='lightgray')
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    locations = [loc for loc in locations if all(elem is not None for elem in loc)]
    for (i, (lon, lat)) in enumerate(locations):
      if lon and lat:
        ax.text(lon+3, lat+3, str(i), color='blue')
    for i in range(len(locations)-1):
      ax.plot([locations[i][0],locations[i+1][0]],[locations[i][1],locations[i+1][1]],color='red',linewidth=2,marker='o')
    plt.savefig('plot.png')

def geolocate(ip):
  response = requests.get(f'http://ip-api.com/json/{ip}')
  data = response.json()
  return data


def traceroute(host):
  command = ['traceroute', '-n', '-w', '10.0,3.0,10.0', host]
  process = subprocess.Popen(command, stdout=subprocess.PIPE)
  first_line = True
  locations = []
  while True:
    line = process.stdout.readline().decode('utf-8')
    if not line:
      break
    if first_line:
      first_line = False
      continue
    data = parse_traceroute_line(line)
    print(line)
    print(data)
    locations.append([data[1], data[2]])
  return(locations)


def parse_traceroute_line(line):
  parts = line.split()
  hop_num = parts[0]
  hop_name = parts[1] if len(parts) > 1 else None
  hop_ip = parts[2].strip('()') if len(parts) > 2 else None
  longitude = None
  latitude = None
  if hop_name != '*':
    data = geolocate(hop_name)
    if data['status'] == 'success':
      longitude = data['lon']
      latitude = data['lat']
  return (hop_num, longitude, latitude, hop_ip)


if __name__ == '__main__':
    plot()
