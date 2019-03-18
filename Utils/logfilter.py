'''Separates the log file by client name'''
import sys
import click
__author__ = "Sam Whang"

# globals -- not a good practice but all functions need it so...
debugprint = False
parentlog = None
filter_on = False

# most, if not all, the names found within the mountainhome log
names = dict()
    # fill in terms that you would like to filter on

def build_logname(name):
    # if filter is on the appends filter string to name of file
    filter_string = ""
    if filter_on:
        filter_string = "_F"
    return name + filter_string + '.txt'
    
def initialize_log_files(name):
    # initialize each file with header text
    # make sure the name of the file we are pulling from has the parent 
    # file as well as the current name being written
    logname = build_logname(name)
    with open(logname, 'w') as log:
        if debugprint:
            print(f"Initializing {logname} for writing...")
        log.write(f"Portion of {parentlog}")
        log.write(f"\t{name}")

def read_parent_log():
    if debugprint:
        print(f"Opening {parentlog} for reading")
    
    with open(parentlog, 'r') as log:
        loglines = log.readlines()
    
    if debugprint:
        print(f"Finished reading {parentlog}")

    return loglines

def write_to_logs():
    for name, logs in names.items():
        # prevents writing an empty log file for a cleaner directory
        if logs:
            initialize_log_files(name)
            write_to_log(name, logs)
        else:
            if debugprint:
                print(f"No logs for {name}. Skipping.")
    
    if debugprint:
        print("Finished writing logs to new files")

def write_to_log(name, messages):
    logname = build_logname(name)
    with open(logname, 'a') as log:
        if debugprint:
            print(f"Writing to {logname}...")
        log.writelines(messages)

def parse_lines_by_name(lines):
    if debugprint: 
        print("Parsing lines...")

    lastusedname = None
    # filter each line based on name in names dictionary
    for line in lines:
        linewritten = False

        # if filter is ON then do not add these lines even if the line
        # contains a term name
        if filter_on and 'TimeoutThread' in line:
            continue

        # check if name is in the log message and write to that log
        for name in names.keys():
            if name in line:
                names[name].append(line)
                lastusedname = name
                linewritten = True

            # it's already written, continue to next line
            if linewritten:
                break

        # handle line if after iterating names, still was not written
        if not linewritten:
            # this is an exception branch to catch unknown names
            if not lastusedname:
                print(line)
                print(any([n in line for n in names]))
                break

            # if line has no name in it (ie, tabbed log msg)
            # append it to the last used file log
            names[lastusedname].append(line)
            
    if debugprint: 
        print("Parsing finished")

@click.command()
@click.option("-f", "logfile")
@click.option("--debug", "debug", default=False, is_flag=True)
@click.option("--filter", "timeoutfilter", default=False, is_flag=True)
def main(logfile, debug, timeoutfilter):
    global debugprint, parentlog, filter_on
    if not logfile:
        print("No file specified. Aborting operation")
        exit(1)

    debugprint = debug
    parentlog = logfile
    filter_on = timeoutfilter
        
    loglines = read_parent_log()
    parse_lines_by_name(loglines)
    write_to_logs()
    print("Done")

if __name__ == "__main__":
    main()
