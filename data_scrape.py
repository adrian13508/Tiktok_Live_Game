import pyautogui
from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import *
import sys


player1_nick = sys.argv[1]
player2_nick = sys.argv[2]
player3_nick = sys.argv[3]
player4_nick = sys.argv[4]
resume_command = sys.argv[5]

client: TikTokLiveClient = TikTokLiveClient(unique_id='@tiktok_live_game', **({ 'enable_extended_gift_info': True}))

@client.on('connect')
async def on_connect(_: ConnectEvent):
    print('Connected to Room ID:', client.room_id)

@client.on('comment')
async def on_connect(event: CommentEvent):

    if event.comment == player1_nick:
        pyautogui.keyDown('1')
        pyautogui.keyUp('1')
    if event.comment == player2_nick:
        pyautogui.keyDown('2')
        pyautogui.keyUp('2')
    if event.comment == player3_nick:
        pyautogui.keyDown('3')
        pyautogui.keyUp('3')
    if event.comment == player4_nick:
        pyautogui.keyDown('4')
        pyautogui.keyUp('4')
    if event.comment == resume_command:
        pyautogui.keyDown('SPACE')
        pyautogui.keyUp('SPACE')
        sys.exit()

    print(f'{event.user.uniqueId} --> {event.comment}')

@client.on('gift')
async def on_gift(event: GiftEvent):
    if event.gift.gift_type == 1 and event.gift.repeat_end == 1:
        print(f"{event.user.uniqueId} sent {event.gift.repeat_count}x \"{event.gift.extended_gift.name}\"")

    # It's not type 1, which means it can't have a streak & is automatically over
    elif event.gift.gift_type != 1:
        print(f"{event.user.uniqueId} sent \"{event.gift.extended_gift.name}\"")

@client.on('like')
async def on_like(event: LikeEvent):
    print(f'{event.user.uniqueId} has liked the stream {event.likeCount} times, there is now {event.totalLikeCount} total likes!')

@client.on('follow')
async def on_follow(event: FollowEvent):
    print(f'{event.user.uniqueId} followed the streamer')

@client.on('share')
async def on_share(event: ShareEvent):
    print(f'{event.user.uniqueId} shared the streamer')

@client.on('viewer_count_update')
async def on_connect(event: ViewerCountUpdateEvent):
    print(f'Received a new viewer count: {event.viewerCount}')

if __name__ == '__main__':

    client.run()

