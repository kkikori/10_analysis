import analysis_funcs
from pathlib import Path

# 結果保存用ファイル名
result_fn = Path("/Users/ida/Amazon Drive/201810結果")


def analysis_main(Week1, Week2):
    print("", len(Week1.random_th_l))
    print("", len(Week2.random_th_l))

    analysis_funcs.facilitator_self(Week1, result_fn / "Week1_facilitator.csv")
    analysis_funcs.facilitator_self(Week2, result_fn / "Week2_facilitator.csv")
