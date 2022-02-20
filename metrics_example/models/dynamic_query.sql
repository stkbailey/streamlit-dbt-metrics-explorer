
        select * from
        {{ 
            metrics.metric(
                metric_name='netflix_releases',
                grain='week',
                dimensions=['show_type'],
                secondary_calculations=[
                    metrics.period_over_period(comparison_strategy="ratio", interval=1),
                    metrics.period_over_period(comparison_strategy="difference", interval=1),
                    metrics.rolling(aggregate="max", interval=4),
                    metrics.rolling(aggregate="min", interval=4)
                ]
            )
        }}
        where period between '2016-01-01':: date and '2021-10-01':: date
        order by period
        