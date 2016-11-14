# Running POX
1. Navigate to pox directory `$ cd ~/pox`
2. Create a softlink to controller file: `$ ln -s ~/submission/controller_ans.py ~/pox/pox/misc/controller.py`
3. Create a softlink to policy file: `$ ln -s ~/submission/policy.in ~/pox/policy.in`
4. Run `$ ./pox.py log.level --DEBUG pox.misc.controller`

# Running Mininet
1. Ensure POX is running first; See above
2. Place `mininetTopo.py` and `topology.in` in `~/submission/` folder
3. Navigate to that folder in command line
4. Run `$ sudo python mininetTopo.py`
