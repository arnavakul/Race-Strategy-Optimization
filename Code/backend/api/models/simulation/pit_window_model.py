#The purpose of this fileis to evaluate optimal pit timinig zone
# -undercut
# -overcut
# -stint extension logic
# -strategic pit timing
def evaluate_pit_window(tyre_age, cliff_age):
    
    window_start = cliff_age - 3
    window_end = cliff_age + 1
    
    if tyre_age < window_start:
        return "TOO_EARLY"
    
    #undercut strategy
    elif tyre_age <= window_start:
        return "UNDERCUT_WINDOW"
    
    #overcut strategy
    elif tyre_age <= window_end:
        return "EXTEND_WINDOW"
    else:
        return "FORCE_PIT"


if __name__ == "__main__":

    result = evaluate_pit_window(

        tyre_age=19,

        cliff_age=20
    )

    print(result)