from pathlib import Path
import vocabulary_funcs


def vocab_usr(Week, save_f, week):
    agent_Type = "claim"
    print("agent type ", agent_Type)
    sav_n = week + agent_Type + "_error_bar.png"
    vocabulary_funcs.only_reply_to_facilitator(Week.claim_usr_l, Week.claim_post_l, Week.claim_mrph, \
                                               save_f / sav_n)

    agent_Type = "random"
    print("agent type ", agent_Type)
    sav_n = week + agent_Type + "_error_bar.png"
    vocabulary_funcs.only_reply_to_facilitator(Week.random_usr_l, Week.random_post_l, Week.random_mrph, \
                                               save_f / sav_n)


def vocab_main(Week1, Week2):
    # 結果保存用ファイル名
    result_fn = Path("/Users/ida/Amazon Drive/201810結果/Vocabs")

    vocab_usr(Week1, result_fn / "vocab_only_rep2f", "Agroup")
    vocab_usr(Week2, result_fn / "vocab_only_rep2f", "Bgroup")
