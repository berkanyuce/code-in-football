from mplsoccer import Pitch
from statsbombpy import sb

competitions = sb.competitions()

competition_id = 43
season_id = 106

matches = sb.matches(competition_id=competition_id, season_id=season_id)

match_id = 3869685
events = sb.events(match_id=match_id)

team1, team2 = events['team'].unique()

mask_team1 = (events['type'] == 'Pass') & (events['team'] == team1)

df_pass = events.loc[mask_team1, ['location', 'pass_end_location', 'pass_outcome']].reset_index(drop=True)

df_pass['x'] = [item[0] for item in df_pass['location']]
df_pass['y'] = [item[1] for item in df_pass['location']]


df_pass['end_x'] = [item[0] for item in df_pass['pass_end_location']]
df_pass['end_y'] = [item[1] for item in df_pass['pass_end_location']]

df_pass.drop(['location', 'pass_end_location'], axis=1, inplace=True)

mask_complete = df_pass.pass_outcome.isnull()

pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc')

fig, ax = pitch.draw(figsize=(16,11), constrained_layout=True, tight_layout=False)

fig.set_facecolor('#22312b')


pitch.arrows(df_pass[mask_complete].x, df_pass[mask_complete].y, df_pass[mask_complete].end_x, df_pass[mask_complete].end_y,
             width=2, headwidth=10, headlength=10, color='#ad993c', ax=ax, label='completed passes')
             


pitch.arrows(df_pass[~mask_complete].x, df_pass[~mask_complete].y, df_pass[~mask_complete].end_x, df_pass[~mask_complete].end_y,
             width=2, headwidth=10, headlength=10, color='#ba4f45', ax=ax, label='other passes')


ax.legend(facecolor='#22312b', handlelength=5, edgecolor='None', fontsize=20, loc='upper left')

ax_title = ax.set_title(f'{team1} passes vs {team2}', fontsize=30)