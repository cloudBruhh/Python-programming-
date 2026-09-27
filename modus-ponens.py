def print_modus_ponens_truth_table():
    print(f"{'P':<6} | {'Q':<6} | {'P -> Q':<8} | {'Q (Conclusion)':<16}")
    print("-" * 45)

    for P in [True, False]:
        for Q in [True, False]:
            # P -> Q is False only when P is True and Q is False
            p_implies_q = (not P) or Q

            # Format outputs for easy reading
            p_str = "T" if P else "F"
            q_str = "T" if Q else "F"
            imp_str = "T" if p_implies_q else "F"
            conc_str = "T" if Q else "F"

            print(f"{p_str:<6} | {q_str:<6} | {imp_str:<8} | {conc_str:<16}")


print_modus_ponens_truth_table()
