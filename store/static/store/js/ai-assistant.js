document.addEventListener('DOMContentLoaded', () => {
    const modalOverlay = document.getElementById('ai-modal');
    const closeModalBtn = document.getElementById('close-ai-modal');
    const aiTriggers = document.querySelectorAll('.open-ai-btn');

    aiTriggers.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const productId = e.target.dataset.productId || '';
            openAiModal(productId);
        });
    });

    if(closeModalBtn) {
        closeModalBtn.addEventListener('click', () => {
            modalOverlay.style.display = 'none';
        });
    }

    function openAiModal(productId) {
        modalOverlay.style.display = 'flex';
        document.getElementById('ai-reasoning').innerText = 'Generating AI insights based on shopping behavior...';
        document.getElementById('similar-products-container').innerHTML = 'Loading recommendations...';

        fetch(`/api/ai-recommendations/?product_id=${productId}`)
            .then(res => res.json())
            .then(data => {
                document.getElementById('ai-reasoning').innerText = data.explanation;
                
                let html = '<h4>Similar & Recommended Products:</h4><div class="product-grid">';
                data.similar_products.forEach(prod => {
                    html += `
                        <div class="product-card">
                            <h5>${prod.name}</h5>
                            <p>$${prod.price}</p>
                            <a href="/product/${prod.slug}/" class="btn">View Details</a>
                        </div>
                    `;
                });
                html += '</div>';
                document.getElementById('similar-products-container').innerHTML = html;
            })
            .catch(err => {
                document.getElementById('ai-reasoning').innerText = 'Failed to load recommendations.';
            });
    }
});