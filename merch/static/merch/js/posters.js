// NIN Posters Gallery JavaScript

let allPosters = null;
let currentPosterIndex = 0;

function openGallery(posterId) {
    // Fetch gallery data via AJAX
    $.ajax({
        url: `/poster-gallery/${posterId}/`,
        type: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        },
        success: function(data) {
            allPosters = data.posters;
            currentPosterIndex = data.initial_index;
            showCurrentPoster();
            $('#galleryModal').addClass('active');
        },
        error: function() {
            alert('Error loading gallery');
        }
    });
}

function showCurrentPoster() {
    if (!allPosters || allPosters.length === 0) return;
    
    const currentPoster = allPosters[currentPosterIndex];
    $('#galleryImage').attr('src', currentPoster.url);
    
    // Use "anonymous" if no submitter name provided
    const submitterName = currentPoster.submitter_name || 'anonymous';
    $('#gallerySubmitter').text(`Submitted by: ${submitterName}`);
    
    // Navigation buttons are never disabled with wrap-around
    $('#galleryPrev').prop('disabled', false);
    $('#galleryNext').prop('disabled', false);
}

function nextPoster() {
    if (allPosters.length === 0) return;
    
    // Wrap around: if at last poster, go to first
    currentPosterIndex = (currentPosterIndex + 1) % allPosters.length;
    showCurrentPoster();
}

function prevPoster() {
    if (allPosters.length === 0) return;
    
    // Wrap around: if at first poster, go to last
    currentPosterIndex = (currentPosterIndex - 1 + allPosters.length) % allPosters.length;
    showCurrentPoster();
}

function closeGallery() {
    $('#galleryModal').removeClass('active');
    allPosters = null;
    currentPosterIndex = 0;
}

// Touch/swipe support for mobile
let touchStartX = 0;
let touchStartY = 0;
let touchEndX = 0;
let touchEndY = 0;

function handleSwipe() {
    const deltaX = touchEndX - touchStartX;
    const deltaY = touchEndY - touchStartY;
    const minSwipeDistance = 50;
    
    // Make sure this is a horizontal swipe (more horizontal than vertical)
    if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > minSwipeDistance) {
        if (deltaX > 0) {
            // Swipe right - go to previous poster
            prevPoster();
        } else {
            // Swipe left - go to next poster
            nextPoster();
        }
    }
}

$(document).ready(function() {
    // Gallery navigation event handlers with mobile optimization
    $('#galleryNext').on('click touchend', function(e) {
        e.preventDefault();
        e.stopPropagation();
        nextPoster();
    });
    
    $('#galleryPrev').on('click touchend', function(e) {
        e.preventDefault();
        e.stopPropagation();
        prevPoster();
    });
    
    $('#galleryClose').on('click touchend', function(e) {
        e.preventDefault();
        e.stopPropagation();
        closeGallery();
    });
    
    // Close gallery when clicking outside the image
    $('#galleryModal').click(function(e) {
        if (e.target === this) {
            closeGallery();
        }
    });
    
    // Keyboard navigation
    $(document).keydown(function(e) {
        if ($('#galleryModal').hasClass('active')) {
            switch(e.keyCode) {
                case 37: // Left arrow
                    prevPoster();
                    break;
                case 39: // Right arrow
                    nextPoster();
                    break;
                case 27: // Escape
                    closeGallery();
                    break;
            }
        }
    });

    // Touch/swipe support
    $('#galleryModal').on('touchstart', function(e) {
        if ($('#galleryModal').hasClass('active')) {
            touchStartX = e.originalEvent.changedTouches[0].screenX;
            touchStartY = e.originalEvent.changedTouches[0].screenY;
        }
    });

    $('#galleryModal').on('touchend', function(e) {
        if ($('#galleryModal').hasClass('active')) {
            touchEndX = e.originalEvent.changedTouches[0].screenX;
            touchEndY = e.originalEvent.changedTouches[0].screenY;
            handleSwipe();
        }
    });

    // Prevent default touch behaviors on gallery image to avoid conflicts
    $('#galleryImage').on('touchstart touchmove touchend', function(e) {
        // Allow default for pinch zoom, but prevent scrolling
        if (e.originalEvent.touches && e.originalEvent.touches.length === 1) {
            e.preventDefault();
        }
    });
    
    // Prevent touch events on navigation buttons from interfering with swipes
    $('.gallery-nav, .gallery-close').on('touchstart touchmove', function(e) {
        e.stopPropagation();
    });
});