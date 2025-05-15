from source import *

def main():
    ndp = NDPDepthChart([2024], 18)
    espn = ESPNDepthChart()
    sc = Schedules([2025])
    st = Statistics([2024])
    e = Excel("output.xlsm")
    e.output_dfs(ndp.get_depth_charts(), "Depth Chart NDP")
    e.output_dfs(espn.get_depth_charts(), "Depth Chart ESPN")
    e.output_dfs(sc.get_schedules(), "Schedules")
    e.output_dfs(st.get_statistics(), "Stats")
    e.close()

if __name__ == '__main__':
    main()