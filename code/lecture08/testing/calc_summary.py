def calc_tips_summary(df):
    df["tip_pct"] = df.tip / df.total_bill
    summary = (
        df.groupby("day")
        .agg(
            count=("tip", "size"),
            avg_bill=("total_bill", "mean"),
            avg_tip=("tip", "mean"),
            avg_tip_pct=("tip_pct", "mean"),
        )
        .round(2)
        .reset_index()
    )
    return summary
