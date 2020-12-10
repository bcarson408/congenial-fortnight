import pandas as pd
import pdb;pdb.set_trace()

fo_qb_ratings_2019_url='https://www.footballoutsiders.com/stats/nfl/qb/2019'
fo_qb_ratings_2018_url='https://www.footballoutsiders.com/stats/nfl/qb/2018'
fo_qb_ratings_2017_url='https://www.footballoutsiders.com/stats/nfl/qb/2017'
fo_rb_ratings_2019_url='https://www.footballoutsiders.com/stats/nfl/rb/2019'
fo_rb_ratings_2018_url='https://www.footballoutsiders.com/stats/nfl/rb/2018'
fo_rb_ratings_2017_url='https://www.footballoutsiders.com/stats/nfl/rb/2017'
fo_wr_ratings_2019_url='https://www.footballoutsiders.com/stats/nfl/wr/2019'
fo_wr_ratings_2018_url='https://www.footballoutsiders.com/stats/nfl/wr/2018'
fo_wr_ratings_2017_url='https://www.footballoutsiders.com/stats/nfl/wr/2017'
fo_te_ratings_2019_url='https://www.footballoutsiders.com/stats/nfl/te/2019'
fo_te_ratings_2018_url='https://www.footballoutsiders.com/stats/nfl/te/2019'
fo_te_ratings_2017_url='https://www.footballoutsiders.com/stats/nfl/te/2019'





# https://www.fantasypros.com/nfl/stats/qb.php?scoring=PPR&year=2017
# team_dvoa_def_dfs  = pd.read_html("https://www.footballoutsiders.com/stats/nfl/team-defense/2019")
# print(len(team_dvoa_def_dfs))
# team_dvoa_def_df = team_dvoa_def_dfs[0]

def create_stat_file(url_text):
    url_list = url_text.split('/')
    site_name = url_list[2].split('.')[1]
    position_year = "_".join(url_list[3:])
    return(site_name+"_"+position_year)

def get_dfs(url):
    count = 0
    ext=".csv"
    dfs = pd.read_html(url)
    for df in dfs:
         file = create_stat_file(url)
         if count <= 0:
             file = file+ext
             df.to_csv(file,index=False)
         else:
            file = file+"_"+str(count)+ext
            df.to_csv(file,index=False)
         count += 1

def main():
    # get_dfs(fo_rb_ratings_2018_url)
    # get_dfs(fo_rb_ratings_2017_url)
    # get_dfs(fo_wr_ratings_2019_url)
    # get_dfs(fo_wr_ratings_2018_url)
    # get_dfs(fo_wr_ratings_2017_url)
    # get_dfs(fo_te_ratings_2019_url)
    # get_dfs(fo_te_ratings_2018_url)
    # get_dfs(fo_te_ratings_2017_url)
def fantasypros_stats():
    base_url = 'https://www.fantasypros.com/nfl/stats/'
    positions = ['qb','rb','wr','te','dst','dl','lb','db']
    years = ['2017','2018','2019']
    for pos in positions:
        base_url_pos = base_url+pos+'.php'
        for year in years:
            base_url_pos_year = base_url_pos+'?scoring=PPR&year='+year
            get_dfs(base_url_pos_year)

if __name__ == "__main__":
    main()
