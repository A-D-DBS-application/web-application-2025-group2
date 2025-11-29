import React, { useState } from 'react';
import { Search, MapPin, Star, SlidersHorizontal, X } from 'lucide-react';
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
  reviews: number;
}

const mockPhotographers: Photographer[] = [
  {
    id: '1',
    name: 'Emma van Bergen',
    location: 'Amsterdam',
    specialty: 'Portrait & Wedding',
    bio: 'Capturing authentic moments with a natural, documentary style.',
    hourlyRate: 150,
    portfolioImages: ['https://images.unsplash.com/photo-1519741497674-611481863552', 'https://images.unsplash.com/photo-1606216794074-735e91aa2c92', 'https://images.unsplash.com/photo-1511285560929-80b456fea0bc'],
    profileImage: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330',
    totalBookings: 127,
    rating: 4.9,
    reviews: 127
  },
  {
    id: '2',
    name: 'Thomas de Vries',
    location: 'Rotterdam',
    specialty: 'Commercial & Product',
    bio: 'Specializing in product photography with creative lighting techniques.',
    hourlyRate: 120,
    portfolioImages: ['https://images.unsplash.com/photo-1542038784456-1ea8e935640e', 'https://images.unsplash.com/photo-1523275335684-37898b6baf30', 'https://images.unsplash.com/photo-1572635196237-14b3f281503f'],
    profileImage: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d',
    totalBookings: 94,
    rating: 4.8,
    reviews: 94
  },
  {
    id: '3',
    name: 'Sophie Janssen',
    location: 'Utrecht',
    specialty: 'Nature & Landscape',
    bio: 'Bringing the beauty of nature to life through my lens.',
    hourlyRate: 100,
    portfolioImages: ['https://images.unsplash.com/photo-1506905925346-21bda4d32df4', 'https://images.unsplash.com/photo-1469474968028-56623f02e42e', 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e'],
    profileImage: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80',
    totalBookings: 73,
    rating: 5.0,
    reviews: 73
  },
  {
    id: '4',
    name: 'Lucas Bakker',
    location: 'The Hague',
    specialty: 'Event & Corporate',
    bio: 'Professional event coverage with attention to detail.',
    hourlyRate: 180,
    portfolioImages: ['https://images.unsplash.com/photo-1511578314322-379afb476865', 'https://images.unsplash.com/photo-1540575467063-178a50c2df87', 'https://images.unsplash.com/photo-1505236858219-8359eb29e329'],
    profileImage: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e',
    totalBookings: 112,
    rating: 4.7,
    reviews: 112
  },
  {
    id: '5',
    name: 'Nina Vermeer',
    location: 'Amsterdam',
    specialty: 'Fashion & Editorial',
    bio: 'Creating bold, editorial images that tell compelling stories.',
    hourlyRate: 200,
    portfolioImages: ['https://images.unsplash.com/photo-1509631179647-0177331693ae', 'https://images.unsplash.com/photo-1485968579580-b6d095142e6e', 'https://images.unsplash.com/photo-1483985988355-763728e1935b'],
    profileImage: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb',
    totalBookings: 156,
    rating: 4.9,
    reviews: 156
  },
  {
    id: '6',
    name: 'Max Koning',
    location: 'Eindhoven',
    specialty: 'Architecture & Real Estate',
    bio: 'Showcasing spaces through architectural photography excellence.',
    hourlyRate: 140,
    portfolioImages: ['https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b', 'https://images.unsplash.com/photo-1565183928294-7d22f6d4fc08', 'https://images.unsplash.com/photo-1512918728675-ed5a9ecdebfd'],
    profileImage: 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d',
    totalBookings: 89,
    rating: 4.8,
    reviews: 89
  }
];

interface PhotographersDirectoryProps {
  onViewProfile: (photographerId: string) => void;
}

export default function PhotographersDirectory({ onViewProfile }: PhotographersDirectoryProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedSpecialty, setSelectedSpecialty] = useState('All');
  const [priceRange, setPriceRange] = useState([0, 500]);
  const [minRating, setMinRating] = useState(0);
  const [showFilters, setShowFilters] = useState(false);

  const specialties = [
    'All',
    'Portrait & Wedding',
    'Commercial & Product',
    'Nature & Landscape',
    'Event & Corporate',
    'Fashion & Editorial',
    'Architecture & Real Estate'
  ];

  const filteredPhotographers = mockPhotographers.filter(photographer => {
    const matchesSearch = photographer.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         photographer.location.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesSpecialty = selectedSpecialty === 'All' || photographer.specialty === selectedSpecialty;
    const matchesPrice = photographer.hourlyRate >= priceRange[0] && photographer.hourlyRate <= priceRange[1];
    const matchesRating = photographer.rating >= minRating;
    return matchesSearch && matchesSpecialty && matchesPrice && matchesRating;
  });

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#F1F5F9' }}>
      {/* Header Section */}
      <div style={{
        backgroundColor: '#FFFFFF',
        borderBottom: '1px solid #E2E8F0',
        padding: '3rem 2rem'
      }}>
        <div style={{ maxWidth: '1280px', margin: '0 auto' }}>
          <h1 style={{
            fontSize: '2.5rem',
            fontWeight: '700',
            color: '#1E293B',
            marginBottom: '1rem',
            textAlign: 'center'
          }}>
            Find Your Perfect Photographer
          </h1>
          <p style={{
            fontSize: '1.125rem',
            color: '#64748B',
            textAlign: 'center',
            maxWidth: '600px',
            margin: '0 auto 2rem'
          }}>
            Browse {mockPhotographers.length} talented photographers ready to capture your moments
          </p>

          {/* Search and Filter Bar */}
          <div style={{
            display: 'flex',
            gap: '1rem',
            maxWidth: '800px',
            margin: '0 auto',
            flexWrap: 'wrap'
          }}>
            <div style={{
              flex: 1,
              minWidth: '300px',
              position: 'relative'
            }}>
              <Search
                size={20}
                color="#94A3B8"
                style={{
                  position: 'absolute',
                  left: '1rem',
                  top: '50%',
                  transform: 'translateY(-50%)',
                  pointerEvents: 'none'
                }}
              />
              <input
                type="text"
                placeholder="Search by name or location..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                style={{
                  width: '100%',
                  padding: '0.875rem 1rem 0.875rem 3rem',
                  border: '2px solid #E2E8F0',
                  borderRadius: '12px',
                  fontSize: '1rem',
                  outline: 'none',
                  transition: 'all 0.2s ease',
                  backgroundColor: '#FFFFFF'
                }}
                onFocus={(e) => {
                  e.target.style.borderColor = '#2563EB';
                  e.target.style.boxShadow = '0 0 0 4px rgba(37, 99, 235, 0.1)';
                }}
                onBlur={(e) => {
                  e.target.style.borderColor = '#E2E8F0';
                  e.target.style.boxShadow = 'none';
                }}
              />
            </div>
            <button
              onClick={() => setShowFilters(!showFilters)}
              style={{
                padding: '0.875rem 1.5rem',
                backgroundColor: showFilters ? '#2563EB' : '#FFFFFF',
                color: showFilters ? '#FFFFFF' : '#1E293B',
                border: '2px solid #E2E8F0',
                borderRadius: '12px',
                fontWeight: '600',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                transition: 'all 0.2s ease'
              }}
              onMouseEnter={(e) => {
                if (!showFilters) e.currentTarget.style.backgroundColor = '#F1F5F9';
              }}
              onMouseLeave={(e) => {
                if (!showFilters) e.currentTarget.style.backgroundColor = '#FFFFFF';
              }}
            >
              <SlidersHorizontal size={20} />
              Filters
            </button>
          </div>
        </div>
      </div>

      {/* Filters Panel */}
      {showFilters && (
        <div style={{
          backgroundColor: '#FFFFFF',
          borderBottom: '1px solid #E2E8F0',
          padding: '2rem'
        }}>
          <div style={{ maxWidth: '1280px', margin: '0 auto' }}>
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
              gap: '2rem'
            }}>
              {/* Specialty Filter */}
              <div>
                <label style={{
                  display: 'block',
                  fontSize: '0.875rem',
                  fontWeight: '600',
                  color: '#1E293B',
                  marginBottom: '0.75rem'
                }}>
                  Photography Type
                </label>
                <select
                  value={selectedSpecialty}
                  onChange={(e) => setSelectedSpecialty(e.target.value)}
                  style={{
                    width: '100%',
                    padding: '0.75rem',
                    border: '2px solid #E2E8F0',
                    borderRadius: '8px',
                    fontSize: '1rem',
                    cursor: 'pointer',
                    outline: 'none',
                    backgroundColor: '#FFFFFF'
                  }}
                >
                  {specialties.map(specialty => (
                    <option key={specialty} value={specialty}>{specialty}</option>
                  ))}
                </select>
              </div>

              {/* Price Range */}
              <div>
                <label style={{
                  display: 'block',
                  fontSize: '0.875rem',
                  fontWeight: '600',
                  color: '#1E293B',
                  marginBottom: '0.75rem'
                }}>
                  Price Range: €{priceRange[0]} - €{priceRange[1]}/hr
                </label>
                <input
                  type="range"
                  min="0"
                  max="500"
                  value={priceRange[1]}
                  onChange={(e) => setPriceRange([0, parseInt(e.target.value)])}
                  style={{
                    width: '100%',
                    cursor: 'pointer'
                  }}
                />
              </div>

              {/* Rating Filter */}
              <div>
                <label style={{
                  display: 'block',
                  fontSize: '0.875rem',
                  fontWeight: '600',
                  color: '#1E293B',
                  marginBottom: '0.75rem'
                }}>
                  Minimum Rating
                </label>
                <div style={{ display: 'flex', gap: '0.5rem' }}>
                  {[0, 3, 4, 4.5, 5].map(rating => (
                    <button
                      key={rating}
                      onClick={() => setMinRating(rating)}
                      style={{
                        padding: '0.5rem 1rem',
                        backgroundColor: minRating === rating ? '#2563EB' : '#F1F5F9',
                        color: minRating === rating ? '#FFFFFF' : '#1E293B',
                        border: 'none',
                        borderRadius: '8px',
                        fontWeight: '600',
                        cursor: 'pointer',
                        fontSize: '0.875rem',
                        transition: 'all 0.2s ease'
                      }}
                    >
                      {rating === 0 ? 'Any' : `${rating}+`}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Results */}
      <div style={{
        maxWidth: '1280px',
        margin: '0 auto',
        padding: '3rem 2rem'
      }}>
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '2rem'
        }}>
          <h2 style={{
            fontSize: '1.5rem',
            fontWeight: '600',
            color: '#1E293B'
          }}>
            {filteredPhotographers.length} Photographers Available
          </h2>
        </div>

        {filteredPhotographers.length === 0 ? (
          <div style={{
            textAlign: 'center',
            padding: '4rem 2rem',
            backgroundColor: '#FFFFFF',
            borderRadius: '16px'
          }}>
            <p style={{
              fontSize: '1.125rem',
              color: '#64748B'
            }}>
              No photographers found matching your criteria
            </p>
            <button
              onClick={() => {
                setSearchTerm('');
                setSelectedSpecialty('All');
                setPriceRange([0, 500]);
                setMinRating(0);
              }}
              style={{
                marginTop: '1rem',
                padding: '0.75rem 1.5rem',
                backgroundColor: '#2563EB',
                color: '#FFFFFF',
                border: 'none',
                borderRadius: '8px',
                fontWeight: '600',
                cursor: 'pointer'
              }}
            >
              Clear Filters
            </button>
          </div>
        ) : (
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))',
            gap: '2rem'
          }}>
            {filteredPhotographers.map(photographer => (
              <div
                key={photographer.id}
                onClick={() => onViewProfile(photographer.id)}
                style={{
                  backgroundColor: '#FFFFFF',
                  borderRadius: '16px',
                  overflow: 'hidden',
                  boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
                  cursor: 'pointer',
                  transition: 'all 0.3s ease'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = 'translateY(-4px)';
                  e.currentTarget.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.15)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = 'translateY(0)';
                  e.currentTarget.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.1)';
                }}
              >
                {/* Portfolio Preview */}
                <div style={{
                  position: 'relative',
                  paddingBottom: '75%',
                  backgroundColor: '#F1F5F9'
                }}>
                  <ImageWithFallback
                    src={photographer.portfolioImages[0]}
                    alt={photographer.name}
                    style={{
                      position: 'absolute',
                      top: 0,
                      left: 0,
                      width: '100%',
                      height: '100%',
                      objectFit: 'cover'
                    }}
                  />
                  <div style={{
                    position: 'absolute',
                    top: '1rem',
                    right: '1rem',
                    backgroundColor: '#FFFFFF',
                    borderRadius: '8px',
                    padding: '0.5rem 0.75rem',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.25rem',
                    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.15)'
                  }}>
                    <Star size={14} fill="#F59E0B" color="#F59E0B" />
                    <span style={{
                      fontSize: '0.875rem',
                      fontWeight: '600',
                      color: '#1E293B'
                    }}>
                      {photographer.rating}
                    </span>
                  </div>
                </div>

                {/* Info */}
                <div style={{ padding: '1.5rem' }}>
                  <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '1rem',
                    marginBottom: '1rem'
                  }}>
                    <ImageWithFallback
                      src={photographer.profileImage}
                      alt={photographer.name}
                      style={{
                        width: '56px',
                        height: '56px',
                        borderRadius: '12px',
                        objectFit: 'cover',
                        border: '3px solid #DBEAFE'
                      }}
                    />
                    <div style={{ flex: 1 }}>
                      <h3 style={{
                        fontSize: '1.25rem',
                        fontWeight: '600',
                        color: '#1E293B',
                        marginBottom: '0.25rem'
                      }}>
                        {photographer.name}
                      </h3>
                      <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '0.25rem',
                        color: '#64748B',
                        fontSize: '0.875rem'
                      }}>
                        <MapPin size={14} />
                        <span>{photographer.location}</span>
                      </div>
                    </div>
                  </div>

                  <div style={{
                    display: 'inline-block',
                    padding: '0.375rem 0.75rem',
                    backgroundColor: '#DBEAFE',
                    color: '#2563EB',
                    borderRadius: '6px',
                    fontSize: '0.8125rem',
                    fontWeight: '600',
                    marginBottom: '0.75rem'
                  }}>
                    {photographer.specialty}
                  </div>

                  <p style={{
                    fontSize: '0.9375rem',
                    color: '#64748B',
                    lineHeight: '1.5',
                    marginBottom: '1rem'
                  }}>
                    {photographer.bio}
                  </p>

                  <div style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    paddingTop: '1rem',
                    borderTop: '1px solid #E2E8F0'
                  }}>
                    <div>
                      <div style={{
                        fontSize: '1.5rem',
                        fontWeight: '700',
                        color: '#1E293B'
                      }}>
                        €{photographer.hourlyRate}
                      </div>
                      <div style={{
                        fontSize: '0.75rem',
                        color: '#64748B'
                      }}>
                        per hour
                      </div>
                    </div>
                    <div style={{
                      textAlign: 'right',
                      fontSize: '0.875rem',
                      color: '#64748B'
                    }}>
                      <div>{photographer.reviews} reviews</div>
                      <div>{photographer.totalBookings} bookings</div>
                    </div>
                  </div>

                  <button
                    style={{
                      width: '100%',
                      marginTop: '1rem',
                      padding: '0.75rem',
                      backgroundColor: '#2563EB',
                      color: '#FFFFFF',
                      border: 'none',
                      borderRadius: '8px',
                      fontWeight: '600',
                      cursor: 'pointer',
                      transition: 'all 0.2s ease'
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.backgroundColor = '#1E40AF';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.backgroundColor = '#2563EB';
                    }}
                  >
                    View Profile
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
