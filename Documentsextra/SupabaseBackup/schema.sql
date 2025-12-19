-- Supabase Database Schema
-- Photography Booking Platform
-- Created: 2025-12-19

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- User Table
CREATE TABLE IF NOT EXISTS public.user (
  id integer NOT NULL DEFAULT nextval('user_id_seq'::regclass),
  username character varying NOT NULL UNIQUE,
  role text DEFAULT 'client'::text,
  name character varying,
  email character varying UNIQUE,
  password_hash character varying,
  created_at timestamp without time zone DEFAULT now(),
  CONSTRAINT user_pkey PRIMARY KEY (id)
);

-- Bookings Table
CREATE TABLE IF NOT EXISTS public.bookings (
  id uuid NOT NULL DEFAULT uuid_generate_v4(),
  booking_date_and_time timestamp with time zone NOT NULL,
  type text NOT NULL,
  description text,
  created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  photographer_id integer,
  client_id integer NOT NULL,
  status text DEFAULT 'pending'::text,
  CONSTRAINT bookings_pkey PRIMARY KEY (id),
  CONSTRAINT bookings_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.user(id)
);

-- Album Table
CREATE TABLE IF NOT EXISTS public.album (
  id integer NOT NULL DEFAULT nextval('album_id_seq'::regclass),
  photographer_id integer NOT NULL,
  name character varying NOT NULL,
  description text,
  created_at timestamp without time zone NOT NULL,
  CONSTRAINT album_pkey PRIMARY KEY (id),
  CONSTRAINT album_photographer_id_fkey FOREIGN KEY (photographer_id) REFERENCES public.user(id)
);

-- Photo Table
CREATE TABLE IF NOT EXISTS public.photo (
  photo_id integer NOT NULL DEFAULT nextval('photo_photo_id_seq1'::regclass),
  user_id integer NOT NULL,
  image_url text NOT NULL,
  uploaded_at timestamp without time zone NOT NULL,
  photographer_id integer,
  booking_id uuid,
  title character varying,
  album_id integer,
  CONSTRAINT photo_pkey PRIMARY KEY (photo_id),
  CONSTRAINT photo_photographer_id_fkey FOREIGN KEY (photographer_id) REFERENCES public.user(id),
  CONSTRAINT photo_booking_id_fkey FOREIGN KEY (booking_id) REFERENCES public.bookings(id),
  CONSTRAINT photo_user_id_fkey1 FOREIGN KEY (user_id) REFERENCES public.user(id),
  CONSTRAINT fk_photo_album FOREIGN KEY (album_id) REFERENCES public.album(id)
);

-- Photographer Availability Table
CREATE TABLE IF NOT EXISTS public.photographer_availability (
  id integer NOT NULL DEFAULT nextval('photographer_availability_id_seq'::regclass),
  photographer_id integer NOT NULL,
  available_date date NOT NULL,
  start_time character varying NOT NULL,
  end_time character varying NOT NULL,
  is_available boolean NOT NULL,
  created_at timestamp without time zone NOT NULL,
  CONSTRAINT photographer_availability_pkey PRIMARY KEY (id),
  CONSTRAINT photographer_availability_photographer_id_fkey FOREIGN KEY (photographer_id) REFERENCES public.user(id)
);

-- Rating Table
CREATE TABLE IF NOT EXISTS public.rating (
  id integer NOT NULL DEFAULT nextval('rating_id_seq'::regclass),
  booking_id uuid NOT NULL,
  client_id integer NOT NULL,
  photographer_id integer NOT NULL,
  rating integer NOT NULL,
  review text,
  created_at timestamp without time zone NOT NULL,
  CONSTRAINT rating_pkey PRIMARY KEY (id),
  CONSTRAINT rating_booking_id_fkey FOREIGN KEY (booking_id) REFERENCES public.bookings(id),
  CONSTRAINT rating_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.user(id),
  CONSTRAINT rating_photographer_id_fkey FOREIGN KEY (photographer_id) REFERENCES public.user(id)
);

-- Create Sequences
CREATE SEQUENCE IF NOT EXISTS user_id_seq;
CREATE SEQUENCE IF NOT EXISTS album_id_seq;
CREATE SEQUENCE IF NOT EXISTS photo_photo_id_seq1;
CREATE SEQUENCE IF NOT EXISTS photographer_availability_id_seq;
CREATE SEQUENCE IF NOT EXISTS rating_id_seq;

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_user_email ON public.user(email);
CREATE INDEX IF NOT EXISTS idx_user_role ON public.user(role);
CREATE INDEX IF NOT EXISTS idx_bookings_client ON public.bookings(client_id);
CREATE INDEX IF NOT EXISTS idx_bookings_photographer ON public.bookings(photographer_id);
CREATE INDEX IF NOT EXISTS idx_bookings_status ON public.bookings(status);
CREATE INDEX IF NOT EXISTS idx_photo_album ON public.photo(album_id);
CREATE INDEX IF NOT EXISTS idx_photo_booking ON public.photo(booking_id);
CREATE INDEX IF NOT EXISTS idx_availability_photographer ON public.photographer_availability(photographer_id);
CREATE INDEX IF NOT EXISTS idx_availability_date ON public.photographer_availability(available_date);
