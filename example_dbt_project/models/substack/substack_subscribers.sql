with source as (
    select * from {{ ref("raw_substack_subscribers") }}
)

select
    -- core data
    subscriber_id :: numeric as subscriber_id
    , subscription_type :: text as subscription_type
    , activity :: integer as activity_rating
    , subscription_date :: timestamp as subscribed_at
    , revenue :: text as revenue
    , paid_upgrade_date :: timestamp as paid_upgrade_at
    , emails_enabled_for_newsletters :: text as emails_enabled_for_newsletter

    -- precomputed metrics
    , comments_all_time :: numeric as comments_all_time
    , comments_last_7_days :: numeric as comments_last_7_days
    , comments_last_30_days :: numeric as comments_last_30_days
    , shares_all_time :: numeric as shares_all_time
    , shares_last_7_days :: numeric as shares_last_7_days
    , shares_last_30_days :: numeric as shares_last_30_days
    , email_opens_all_time :: numeric as email_opens_all_time
    , email_opens_last_7_days :: numeric as email_opens_last_7_days
    , email_opens_last_30_days :: numeric as email_opens_last_30_days
    , unique_emails_seen_all_time :: numeric as unique_emails_seen_all_time
    , unique_emails_seen_last_7_days :: numeric as unique_emails_seen_last_7_days
    , unique_emails_seen_last_30_days :: numeric as unique_emails_seen_last_30_days
    , web_post_views_all_time :: numeric as web_post_views_all_time
    , web_post_views_last_7_days :: numeric as web_post_views_last_7_days
    , web_post_views_last_30_days :: numeric as web_post_views_last_30_days
    , unique_web_post_views_all_time :: numeric as unique_web_post_views_all_time
    , uniuqe_web_post_views_last_7_days :: numeric as uniuqe_web_post_views_last_7_days
    , unique_web_post_views_last_30_days :: numeric as unique_web_post_views_last_30_days
    , subscriptions_gifted :: numeric as subscriptions_gifted
    , subscription_source_free :: text as subscription_source_free
    , subscription_source_paid :: text as subscription_source_paid
    , days_active_last_30_days :: numeric as days_active_last_30_days

    -- custom dimensions
    , comments_all_time > 0 as has_commented
    , email_opens_all_time > 0 as has_opened_email
    , subscriptions_gifted > 0 as has_gifted_subscription
    , days_active_last_30_days > 0 as is_recently_active

from
    source
