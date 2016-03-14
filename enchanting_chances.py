#!/usr/bin/python

# Script to use in BDO to find out the chances of succes when enchanting. 
import sys

DATA_DICT = {'1':[100.0,0,0],'2':[100.0,0,0],'3':[100.0,0,0],'4':[100.0,0,0],
        '5':[100.0,0,0],'6':[100.0,0,0],'7':[100.0,0,0],'8':[20.0,2.5,52.5],
        '9':[17.5,2.0,45.5],'10':[15.0,1.5,37.5],'11':[12.5,1.25,32.5],
        '12':[10.0,0.75,23.5],'13':[7.5,0.63,20.0],'14':[5.0,0.5,17.5],'15':[2.5,0.5,15.0]}

# Take in user data...
def take_usr_input():
    print '*' * 50
    print '-- Black Desert Online Enchanting Chances --'
    print '*' * 50
    target_enchan_lvl = raw_input('Target Enchanting Level: ')
    current_fail_stack = raw_input('Current Fail Stacks: ')
    if not DATA_DICT.get(target_enchan_lvl):
        print 'Sorry that level is not valid, please enter a level - [1-15]'
        sys.exit(1)
    return (target_enchan_lvl, current_fail_stack)


# Do math....
def enchanting_math(data_list, current_fail_stack):
    base_pass_rate = data_list[0]
    per_fail_stack = data_list[1]
    highest_rate = data_list[2]
    # If 100%, skip the math and return 
    if base_pass_rate == 100:
        return base_pass_rate
    # Find the normal rate based on fail stacks
    fail_buffer = float(per_fail_stack) * int(current_fail_stack)
    base_pass_rate = fail_buffer + base_pass_rate
    if base_pass_rate > highest_rate:
        base_pass_rate = highest_rate
    return base_pass_rate


def main():
    target_enchan_lvl, current_fail_stack = take_usr_input()
    data_list = DATA_DICT.get(target_enchan_lvl)
    rate = enchanting_math(data_list, current_fail_stack)
    print 'Pass Rate: %s%%, With %s fail stacks' % (rate, current_fail_stack)

if __name__ == "__main__":
    sys.exit(main())
