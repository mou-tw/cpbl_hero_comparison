import pandas as pd
import numpy as np


def compare_atk(playername, play_year):
    hitter_atk_df = pd.read_csv('./docs/hitter_atk.csv')
    hitter_atk_df.name = hitter_atk_df.name.str.extract(r'(\D+)',expand=False)


    target_player = hitter_atk_df.loc[hitter_atk_df.name == playername].loc[hitter_atk_df.play_year == play_year]

    # 取得該年度的有效資料，有效資料的定義為球員的打席需要大於30場

    t_df = hitter_atk_df[hitter_atk_df.play_year == play_year][list(hitter_atk_df)[7:]]
    t_df = t_df[t_df.打席>30]
    t_df_50 = pd.DataFrame(t_df.median())

    # 決定哪些數據不參與比較/正排序/負排序
    d_cols = ['被三振','雙殺打',]
    a_cols = ['出賽數','打席','打數','打點','得分','安打','一安','二安','三安','全壘打','壘打數','盜壘','上壘率','長打率','打擊率',
             '四壞','故四','盜壘率', '整體攻擊指數']
    n_cols = ['犧短','犧飛','死球','盜壘刺','滾地出局','高飛出局','滾飛出局比',]

    # 產出Q50 and Q75 數據
    t_agg_lst = []
    for i in list(hitter_atk_df)[7:]:
        if i in a_cols or i in n_cols:
            t_agg_lst.append(t_df[i].quantile(0.75))
        else :
            t_agg_lst.append(t_df[i].quantile(0.25))
    t_df_75 = pd.DataFrame(t_agg_lst,index= list(hitter_atk_df)[7:])

    agg_t_df = pd.concat([target_player[list(target_player)[7:]].T,t_df_50,t_df_75],axis=1)

    agg_t_df.columns = ['原始數據','該年度球員中位數成績','該年度球員75分百位數成績']

    # compare
    org_col , compare_col = ['原始數據'] , ['該年度球員中位數成績','該年度球員75分百位數成績']
    for i in org_col:
        for j in compare_col:
            tmp_lst = []
            org_s = agg_t_df[i]
            com_s = agg_t_df[j]
            for d in org_s.index:
                if d in d_cols:
                    tmp_lst.append( "lose" if org_s[d] > com_s[d] else "win" )
                elif d in a_cols:
                    tmp_lst.append( "win" if org_s[d] > com_s[d] else "lose" )
                elif d in n_cols:
                    tmp_lst.append(np.NaN)
            # print(pd.DataFrame(tmp_lst, index= list(hitter_atk_df)[7:]))
            agg_t_df[f'{i}_{j}比較'] = pd.DataFrame(tmp_lst, index= list(hitter_atk_df)[7:])

    agg_t_df = agg_t_df.drop(['該年度球員中位數成績','該年度球員75分百位數成績'],1)
    agg_t_df.index.name = '數據項目'
    agg_t_df.columns.name = '數據類型'
    o_df = pd.concat([target_player[list(target_player)[:7]].T,target_player[list(target_player)[:7]].T,target_player[list(target_player)[:7]].T] ,1)
    o_df.columns = agg_t_df.columns
    f_agg_lst = pd.concat([o_df,agg_t_df])
    f_agg_lst.index.name = '數據項目'
    f_agg_lst.columns.name = '數據類型'

    f_agg_lst.to_csv(f'./docs/{playername}_{play_year}.csv')