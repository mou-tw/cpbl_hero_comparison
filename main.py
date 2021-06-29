from utils.hitter_compare_atk import compare_atk
import click


@click.command()
@click.option('-p', '--player_name', 'player_name',  required=True, type=str)
@click.option('-y', '--play_year', 'play_year',  required=True, type= int)
@click.option('-t', '--type', 'type',  required=True, type=str)
def main(player_name,play_year,type):
    assert type in ['atk','dfs'] , 'should be atk or dfs'
    if type == 'atk':
        compare_atk(player_name, play_year)

if __name__ == "__main__":
    main()
