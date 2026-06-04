def choose_best_strategy(forecasts):
    best_forecasts =  min(forecasts, key=lambda x: x["expected_finish"])
    
    sorted_results = sorted(forecasts, key=lambda x: x["expected_finish"])
    
    best_finish = (
        sorted_results[0]
        ["expected_finish"]
    )

    second_finish = (
        sorted_results[1]
        ["expected_finish"]
    )
    
    finish_gap = (
        second_finish - best_finish
    )
    
    if finish_gap >= 2:
        confidence = "HIGH"
    
    elif finish_gap == 1:
        confidence = "MEDIUM"
    
    else:
        confidence = "LOW"
    
    reason = ("Best expected finish position")
    
    return {

        "recommended_action":
            best_forecasts["action"],

        "expected_finish":
            best_forecasts[
                "expected_finish"
            ],

        "predicted_time":
            best_forecasts[
                "predicted_time"
            ],

        "confidence":
            confidence,

        "reason":
            reason
    }

if __name__ == "__main__":
    
        forecasts = [

        {
            "action":"PIT_NOW",
            "expected_finish":2,
            "predicted_time":5100
        },

        {
            "action":"PIT_PLUS_2",
            "expected_finish":4,
            "predicted_time":5120
        },

        {
            "action":"STAY_OUT",
            "expected_finish":5,
            "predicted_time":5140
        }
    ]
        
        result = choose_best_strategy(
            forecasts
        )

        print(result)