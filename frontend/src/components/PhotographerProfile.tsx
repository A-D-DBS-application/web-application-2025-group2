import React, { useState } from 'react';
import { ArrowLeft, MapPin, Star, Calendar, Camera, Mail, Phone, Award, Clock, CheckCircle } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';

interface Photographer {
  id: string;
  name: string;
  location: string;
  specialty: string;
  bio: string;
  hourlyRate: number;
  portfolioImages: string[];
  profileImage: string;
  totalBookings: number;
  rating: number;
  totalReviews: number;
  experience: string;
  email: string;
  phone: string;
  responseTime: string;
  languages: string[];
}

const mockPhotographer: Photographer = {
  id: '1',
  name: 'Emma van Bergen',
  location: 'Amsterdam, Netherlands',
  specialty: 'Portrait & Wedding',
  bio: 'Capturing authentic moments with a natural, documentary style. I believe in telling your unique story through honest, emotional imagery. With over 8 years of experience, I specialize in creating timeless photos that you\'ll treasure forever. My approach is unobtrusive yet creative, ensuring you look your absolute best while staying true to yourself.',
  hourlyRate: 150,
  portfolioImages: [
    'https://images.unsplash.com/photo-1519741497674-611481863552',
    'https://images.unsplash.com/photo-1606216794074-735e91aa2c92',
    'https://images.unsplash.com/photo-1511285560929-80b456fea0bc',
    'https://images.unsplash.com/photo-1465495976277-4387d4b0b4c6',
    'https://images.unsplash.com/photo-1522673607200-164d1b6ce486',
    'https://images.unsplash.com/photo-1583939003579-730e3918a45a',
    'https://images.unsplash.com/photo-1591604466107-ec97de577aff',
    'https://images.unsplash.com/photo-1529636798458-92182e662485',
    'https://images.unsplash.com/photo-1502086223501-7ea6ecd79368'
  ],
  profileImage: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330',
  totalBookings: 127,
  rating: 4.9,
  totalReviews: 127,
  experience: '8 years',
  email: 'emma@example.com',
  phone: '+31 6 1234 5678',
  responseTime: 'Within 2 hours',
  languages: ['English', 'Dutch', 'German']
};

interface Review {
  id: string;
  clientName: string;
  rating: number;
  comment: string;
  date: string;
  clientAvatar: string;
}

const mockReviews: Review[] = [
  {
    id: '1',
    clientName: 'Sarah Mitchell',
    rating: 5,
    comment: 'Emma was absolutely amazing! She made us feel so comfortable and the photos turned out beautifully. Highly recommend for any wedding or portrait session!',
    date: 'November 2024',
    clientAvatar: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2'
  },
  {
    id: '2',
    clientName: 'James Peterson',
    rating: 5,
    comment: 'Professional, creative, and a pleasure to work with. The wedding photos exceeded our expectations and captured every special moment perfectly.',
    date: 'October 2024',
    clientAvatar: 'https://images.unsplash.com/photo-1547425260-76bcadfb4f2c'
  },
  {
    id: '3',
    clientName: 'Lisa Anderson',
    rating: 4,
    comment: 'Great experience overall. Emma has a wonderful eye for detail and composition. Would definitely book again!',
    date: 'September 2024',
    clientAvatar: 'https://images.unsplash.com/photo-1487412720507-e7ab37603c6f'
  }
];

interface PhotographerProfileProps {
  photographerId: string;
  onBack: () => void;
  onBookSession: (photographerId: string) => void;
}

export default function PhotographerProfile({ photographerId, onBack, onBookSession }: PhotographerProfileProps) {
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const photographer = mockPhotographer;

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#F1F5F9' }}>
      {/* Back Button */}
      <div style={{ backgroundColor: '#FFFFFF', borderBottom: '1px solid #E2E8F0' }}>
        <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '1.5rem 2rem' }}>
          <button
            onClick={onBack}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              background: 'none',
              border: 'none',
              color: '#2563EB',
              fontWeight: '600',
              cursor: 'pointer',
              fontSize: '0.9375rem',
              padding: '0.5rem',
              transition: 'all 0.2s ease'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.color = '#1E40AF';
              e.currentTarget.style.transform = 'translateX(-2px)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.color = '#2563EB';
              e.currentTarget.style.transform = 'translateX(0)';
            }}
          >
            <ArrowLeft size={20} />
            Back to Directory
          </button>
        </div>
      </div>

      {/* Profile Header */}
      <div style={{ backgroundColor: '#FFFFFF', marginBottom: '2rem' }}>
        <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '3rem 2rem' }}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '3rem', alignItems: 'start' }}>
            {/* Profile Image & Quick Info */}
            <div>
              <ImageWithFallback
                src={photographer.profileImage}
                alt={photographer.name}
                style={{
                  width: '100%',
                  aspectRatio: '1',
                  borderRadius: '16px',
                  objectFit: 'cover',
                  marginBottom: '1.5rem',
                  boxShadow: '0 10px 30px rgba(0, 0, 0, 0.1)'
                }}
              />

              {/* Quick Stats */}
              <div style={{
                backgroundColor: '#F1F5F9',
                borderRadius: '12px',
                padding: '1.5rem'
              }}>
                <div style={{
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '1rem'
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                    <div style={{
                      width: '40px',
                      height: '40px',
                      backgroundColor: '#DBEAFE',
                      borderRadius: '8px',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center'
                    }}>
                      <Clock size={20} color="#2563EB" />
                    </div>
                    <div>
                      <div style={{ fontSize: '0.8125rem', color: '#64748B' }}>Response Time</div>
                      <div style={{ fontWeight: '600', color: '#1E293B' }}>{photographer.responseTime}</div>
                    </div>
                  </div>

                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                    <div style={{
                      width: '40px',
                      height: '40px',
                      backgroundColor: '#DBEAFE',
                      borderRadius: '8px',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center'
                    }}>
                      <Award size={20} color="#2563EB" />
                    </div>
                    <div>
                      <div style={{ fontSize: '0.8125rem', color: '#64748B' }}>Experience</div>
                      <div style={{ fontWeight: '600', color: '#1E293B' }}>{photographer.experience}</div>
                    </div>
                  </div>

                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                    <div style={{
                      width: '40px',
                      height: '40px',
                      backgroundColor: '#DBEAFE',
                      borderRadius: '8px',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center'
                    }}>
                      <Camera size={20} color="#2563EB" />
                    </div>
                    <div>
                      <div style={{ fontSize: '0.8125rem', color: '#64748B' }}>Total Bookings</div>
                      <div style={{ fontWeight: '600', color: '#1E293B' }}>{photographer.totalBookings}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Main Info */}
            <div>
              <div style={{
                display: 'inline-block',
                padding: '0.5rem 1rem',
                backgroundColor: '#DBEAFE',
                color: '#1E3A8A',
                borderRadius: '8px',
                fontSize: '0.875rem',
                fontWeight: '600',
                marginBottom: '1rem'
              }}>
                {photographer.specialty}
              </div>

              <h1 style={{
                fontSize: '2.5rem',
                fontWeight: '700',
                color: '#1E293B',
                marginBottom: '1rem'
              }}>
                {photographer.name}
              </h1>

              <div style={{
                display: 'flex',
                flexWrap: 'wrap',
                gap: '1.5rem',
                marginBottom: '1.5rem',
                fontSize: '0.9375rem'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#64748B' }}>
                  <MapPin size={18} />
                  <span>{photographer.location}</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <Star size={18} fill="#F59E0B" color="#F59E0B" />
                  <span style={{ fontWeight: '600', color: '#1E293B' }}>
                    {photographer.rating}
                  </span>
                  <span style={{ color: '#64748B' }}>
                    ({photographer.totalReviews} reviews)
                  </span>
                </div>
              </div>

              <p style={{
                fontSize: '1rem',
                color: '#475569',
                lineHeight: '1.7',
                marginBottom: '2rem'
              }}>
                {photographer.bio}
              </p>

              {/* Languages */}
              <div style={{ marginBottom: '2rem' }}>
                <div style={{
                  fontSize: '0.875rem',
                  fontWeight: '600',
                  color: '#1E293B',
                  marginBottom: '0.5rem'
                }}>
                  Languages
                </div>
                <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                  {photographer.languages.map(lang => (
                    <span
                      key={lang}
                      style={{
                        padding: '0.375rem 0.75rem',
                        backgroundColor: '#F1F5F9',
                        borderRadius: '6px',
                        fontSize: '0.875rem',
                        color: '#475569'
                      }}
                    >
                      {lang}
                    </span>
                  ))}
                </div>
              </div>

              {/* Pricing & CTA */}
              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '2rem',
                padding: '2rem',
                backgroundColor: '#F8FAFC',
                borderRadius: '12px',
                border: '2px solid #E2E8F0'
              }}>
                <div>
                  <div style={{
                    fontSize: '2.5rem',
                    fontWeight: '700',
                    color: '#2563EB'
                  }}>
                    €{photographer.hourlyRate}
                  </div>
                  <div style={{
                    fontSize: '0.875rem',
                    color: '#64748B'
                  }}>
                    per hour
                  </div>
                </div>

                <button
                  onClick={() => onBookSession(photographer.id)}
                  style={{
                    flex: 1,
                    padding: '1rem 2rem',
                    backgroundColor: '#2563EB',
                    color: '#FFFFFF',
                    border: 'none',
                    borderRadius: '12px',
                    fontWeight: '600',
                    fontSize: '1.125rem',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '0.5rem',
                    transition: 'all 0.2s ease'
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.backgroundColor = '#1E40AF';
                    e.currentTarget.style.transform = 'scale(1.02)';
                    e.currentTarget.style.boxShadow = '0 10px 20px rgba(37, 99, 235, 0.3)';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.backgroundColor = '#2563EB';
                    e.currentTarget.style.transform = 'scale(1)';
                    e.currentTarget.style.boxShadow = 'none';
                  }}
                >
                  <Calendar size={20} />
                  Book a Session
                </button>
              </div>

              {/* Contact Info */}
              <div style={{
                display: 'flex',
                gap: '1.5rem',
                marginTop: '1.5rem',
                flexWrap: 'wrap'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#64748B' }}>
                  <Mail size={16} />
                  <span style={{ fontSize: '0.875rem' }}>{photographer.email}</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#64748B' }}>
                  <Phone size={16} />
                  <span style={{ fontSize: '0.875rem' }}>{photographer.phone}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '0 2rem 4rem' }}>
        {/* Portfolio Section */}
        <div style={{ marginBottom: '4rem' }}>
          <h2 style={{
            fontSize: '2rem',
            fontWeight: '700',
            color: '#1E293B',
            marginBottom: '2rem'
          }}>
            Portfolio
          </h2>

          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
            gap: '1.5rem'
          }}>
            {photographer.portfolioImages.map((image, index) => (
              <div
                key={index}
                onClick={() => setSelectedImage(image)}
                style={{
                  position: 'relative',
                  paddingBottom: '100%',
                  backgroundColor: '#F1F5F9',
                  borderRadius: '12px',
                  overflow: 'hidden',
                  cursor: 'pointer',
                  boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
                  transition: 'all 0.3s ease'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = 'scale(1.05)';
                  e.currentTarget.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.15)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = 'scale(1)';
                  e.currentTarget.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.1)';
                }}
              >
                <ImageWithFallback
                  src={image}
                  alt={`Portfolio ${index + 1}`}
                  style={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    width: '100%',
                    height: '100%',
                    objectFit: 'cover'
                  }}
                />
              </div>
            ))}
          </div>
        </div>

        {/* Reviews Section */}
        <div>
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginBottom: '2rem'
          }}>
            <h2 style={{
              fontSize: '2rem',
              fontWeight: '700',
              color: '#1E293B'
            }}>
              Client Reviews
            </h2>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Star size={24} fill="#F59E0B" color="#F59E0B" />
              <span style={{
                fontSize: '1.5rem',
                fontWeight: '700',
                color: '#1E293B'
              }}>
                {photographer.rating}
              </span>
              <span style={{ color: '#64748B' }}>
                ({photographer.totalReviews} reviews)
              </span>
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
            {mockReviews.map(review => (
              <div
                key={review.id}
                style={{
                  backgroundColor: '#FFFFFF',
                  borderRadius: '12px',
                  padding: '2rem',
                  boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)'
                }}
              >
                <div style={{
                  display: 'flex',
                  gap: '1rem',
                  marginBottom: '1rem'
                }}>
                  <ImageWithFallback
                    src={review.clientAvatar}
                    alt={review.clientName}
                    style={{
                      width: '48px',
                      height: '48px',
                      borderRadius: '50%',
                      objectFit: 'cover'
                    }}
                  />
                  <div style={{ flex: 1 }}>
                    <div style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'flex-start',
                      marginBottom: '0.5rem'
                    }}>
                      <div style={{
                        fontWeight: '600',
                        color: '#1E293B'
                      }}>
                        {review.clientName}
                      </div>
                      <div style={{
                        fontSize: '0.875rem',
                        color: '#64748B'
                      }}>
                        {review.date}
                      </div>
                    </div>
                    <div style={{
                      display: 'flex',
                      gap: '0.25rem',
                      marginBottom: '0.75rem'
                    }}>
                      {[...Array(5)].map((_, i) => (
                        <Star
                          key={i}
                          size={16}
                          fill={i < review.rating ? '#F59E0B' : 'none'}
                          color={i < review.rating ? '#F59E0B' : '#E2E8F0'}
                        />
                      ))}
                    </div>
                    <p style={{
                      color: '#475569',
                      lineHeight: '1.6',
                      fontSize: '0.9375rem'
                    }}>
                      {review.comment}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Image Lightbox */}
      {selectedImage && (
        <div
          onClick={() => setSelectedImage(null)}
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(0, 0, 0, 0.95)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000,
            padding: '2rem',
            cursor: 'pointer'
          }}
        >
          <ImageWithFallback
            src={selectedImage}
            alt="Full size"
            style={{
              maxWidth: '90%',
              maxHeight: '90%',
              objectFit: 'contain',
              borderRadius: '8px'
            }}
          />
        </div>
      )}
    </div>
  );
}