from source import *

def main():
    ndp = NDPDepthChart([2024], 18)
    espn = ESPNDepthChart()
    sch = Schedules([2025])
    st = Statistics([2024])
    e = Excel("output.xlsm")
    e.output_dfs(ndp.execute(), "Depth Chart NDP")
    e.output_dfs(espn.execute(), "Depth Chart ESPN")
    e.output_dfs(sch.get_team_schedules(), "Schedules")
    e.output_dfs(st.execute(), "Stats")
    e.close()

if __name__ == '__main__':
    main()