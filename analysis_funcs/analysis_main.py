import analysis_funcs
from pathlib import Path

# 結果保存用ファイル名
result_fn = Path("/Users/ida/Amazon Drive/201810結果")


def analysis_main(Week1, Week2):
    print("", len(Week1.random_th_l))
    print("", len(Week2.random_th_l))

    # analysis_funcs.facilitator_self(Week1, result_fn / "Week1_facilitator.csv")
    # analysis_funcs.facilitator_self(Week2, result_fn / "Week2_facilitator.csv")

    # analysis_funcs.reply_to_facilitator(Week1, result_fn / "Week1_reply_to_facilitator.csv")
    # analysis_funcs.reply_to_facilitator(Week2, result_fn / "Week2_reply_to_facilitator.csv")

    # analysis_funcs.time_series_analysis_main(Week1, result_fn, "week1")
    # analysis_funcs.time_series_analysis_main(Week2, result_fn, "week2")


    # analysis_funcs.facilitator_effect_main(Week1, result_fn, "week1")
    # analysis_funcs.facilitator_effect_main(Week2, result_fn, "week2")

    # analysis_funcs.post_nums_main(Week1, result_fn / "post_nums", "week1")
    # analysis_funcs.post_nums_main(Week2, result_fn / "post_nums", "week2")

    # analysis_funcs.test_post_nums(Week1, Week2, result_fn / "post_nums")


    c_f, c_u, r_f, r_u = analysis_funcs.increase_rate_main(Week1, result_fn / "increase_rate", "week1")
    w1 = [c_f, c_u, r_f, r_u]
    c_f, c_u, r_f, r_u = analysis_funcs.increase_rate_main(Week2, result_fn / "increase_rate", "week2")
    w2 = [c_f, c_u, r_f, r_u]

    analysis_funcs.increase_rate_total_compare(w1, w2,result_fn / "increase_rate")
