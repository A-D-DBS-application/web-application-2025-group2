-- SQL script to create the rating table in Supabase
-- Run this in the Supabase SQL Editor

CREATE TABLE IF NOT EXISTS rating (
    id SERIAL PRIMARY KEY,
    booking_id UUID NOT NULL REFERENCES bookings(id) ON DELETE CASCADE,
    client_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    photographer_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    review TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Add index for faster queries
CREATE INDEX IF NOT EXISTS idx_rating_photographer ON rating(photographer_id);
CREATE INDEX IF NOT EXISTS idx_rating_booking ON rating(booking_id);

-- Sample ratings for testing (optional)
INSERT INTO rating (booking_id, client_id, photographer_id, rating, review, created_at) VALUES
    (
        (SELECT id FROM bookings WHERE photographer_id = (SELECT id FROM "user" WHERE email = 'john@photographer.com') LIMIT 1),
        (SELECT id FROM "user" WHERE email = 'alice@client.com'),
        (SELECT id FROM "user" WHERE email = 'john@photographer.com'),
        5,
        'Amazing photographer! Very professional and delivered stunning photos.',
        NOW()
    ),
    (
        (SELECT id FROM bookings WHERE photographer_id = (SELECT id FROM "user" WHERE email = 'emma@photographer.com') LIMIT 1),
        (SELECT id FROM "user" WHERE email = 'bob@client.com'),
        (SELECT id FROM "user" WHERE email = 'emma@photographer.com'),
        4,
        'Great experience, would definitely book again!',
        NOW()
    )
ON CONFLICT DO NOTHING;

SELECT 'Rating table created successfully!' as status;
