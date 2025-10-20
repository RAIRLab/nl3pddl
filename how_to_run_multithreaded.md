if uv isn't installed, run this command

'''
curl -LsSf https://astral.sh/uv/install.sh | sh
'''

then do 
'''uv init'''

and install python 3.13 experimental multithreaded
'''uv python install 3.13t'''

make a venv with the following command
'''uv venv --python 3.13+freethreaded'''

and then
'''uv sync --python 3.13t'''

run '''python test_gil_enabled.py''', and if you see False, you're gtg!
Enjoy the sub 3 minute runs when calling '''python driver -r'''

