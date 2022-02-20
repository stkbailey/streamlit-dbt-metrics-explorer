with source as (
    select * from {{ ref("raw_substack_subscribers") }}
)

select
    subscriber_id :: number as subscriber_id
    , subscription_type :: text as subscription_type
    , activity :: integer as activity_rating
    , subscription_date :: timestamp as subscribed_at
    , revenue :: text as revenue
    , first_payment_at :: timestamp as first_payment_at
    , paid_upgrade_date :: timestamp as paid_upgrade_at
    , cancel_date :: timestamp as cancelled_at
    , emails_enabled_for_newsletter :: text as emails_enabled_for_newsletter
    , comments_all_time :: number as comments_all_time
    , comments_last_7_days :: number as comments_last_7_days
    , comments_last_30_days :: number as comments_last_30_days
    , shares_all_time :: number as shares_all_time
    , shares_last_7_days :: number as shares_last_7_days
    , shares_last_30_days :: number as shares_last_30_days
    , email_opens_all_time :: number as email_opens_all_time
    , email_opens_last_7_days :: number as email_opens_last_7_days
    , email_opens_last_30_days :: number as email_opens_last_30_days
    , unique_emails_seen_all_time :: number as unique_emails_seen_all_time
    , unique_emails_seen_last_7_days :: number as unique_emails_seen_last_7_days
    , unique_emails_seen_last_30_days :: number as unique_emails_seen_last_30_days
    , web_post_views_all_time :: number as web_post_views_all_time
    , web_post_views_last_7_days :: number as web_post_views_last_7_days
    , web_post_views_last_30_days :: number as web_post_views_last_30_days
    , unique_web_post_views_all_time :: number as unique_web_post_views_all_time
    , uniuqe_web_post_views_last_7_days :: number as uniuqe_web_post_views_last_7_days
    , unique_web_post_views_last_30_days :: number as unique_web_post_views_last_30_days
    , subscriptions_gifted :: number as subscriptions_gifted
    , expires_at :: number as expires_at
    , subscription_source_free :: number as subscription_source_free
    , subscription_source_paid :: number as subscription_source_paid
    , days_active_last_30_days :: number as days_active_last_30_days
from
    source