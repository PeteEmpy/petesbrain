// AI-Powered Generation Modals for Google Ads Campaign Builder

document.addEventListener('DOMContentLoaded', function() {
    // Button event listeners
    const generateKeywordsBtn = document.getElementById('generateKeywordsBtn');
    const generateRsaBtn = document.getElementById('generateRsaBtn');
    const generateAssetGroupBtn = document.getElementById('generateAssetGroupBtn');

    if (generateKeywordsBtn) {
        generateKeywordsBtn.addEventListener('click', handleGenerateKeywords);
    }

    if (generateRsaBtn) {
        generateRsaBtn.addEventListener('click', handleGenerateRsa);
    }

    if (generateAssetGroupBtn) {
        generateAssetGroupBtn.addEventListener('click', handleGenerateAssetGroup);
    }
});

// =======================
// KEYWORD GENERATION
// =======================

async function handleGenerateKeywords() {
    const url = document.getElementById('keywords_url').value.trim();
    const client = document.getElementById('client').value;
    const model = document.querySelector('input[name="keywordModel"]:checked').value;

    if (!client) {
        alert('Please select a client first');
        return;
    }

    if (!url) {
        alert('Please enter a landing page URL');
        return;
    }

    // Open modal
    const modal = document.getElementById('keywordModal');
    modal.classList.remove('hidden');

    // Show loading state
    document.getElementById('keywordLoading').classList.remove('hidden');
    document.getElementById('keywordResults').classList.add('hidden');
    document.getElementById('keywordFooter').classList.add('hidden');

    try {
        const response = await fetch('/api/generate_keywords', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                url: url,
                client: client,
                max_keywords: 25,
                model: model
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to generate keywords');
        }

        const data = await response.json();

        // Hide loading, show results
        document.getElementById('keywordLoading').classList.add('hidden');
        document.getElementById('keywordResults').classList.remove('hidden');
        document.getElementById('keywordFooter').classList.remove('hidden');

        // Display results
        displayKeywords(data.keywords, data.stats);

    } catch (error) {
        console.error('Error generating keywords:', error);
        alert(`Error: ${error.message}`);
        closeKeywordModal();
    }
}

function displayKeywords(keywords, stats) {
    const list = document.getElementById('keywordList');
    list.innerHTML = '';

    // Display filter stats
    let statsText = `Generated ${stats.total_generated} keywords`;
    if (stats.filtered_existing > 0 || stats.filtered_pmax > 0) {
        statsText += ` • Filtered ${stats.filtered_existing + stats.filtered_pmax} duplicates`;
        if (stats.filtered_existing > 0) {
            statsText += ` (${stats.filtered_existing} in account`;
        }
        if (stats.filtered_pmax > 0) {
            statsText += stats.filtered_existing > 0 ? `, ${stats.filtered_pmax} in PMax)` : ` (${stats.filtered_pmax} in PMax)`;
        }
        if (stats.filtered_existing > 0 && stats.filtered_pmax === 0) {
            statsText += `)`;
        }
    }
    statsText += ` • Showing ${stats.returned}`;
    document.getElementById('keywordFilterStats').textContent = statsText;

    // Display cost stats
    if (stats.cost !== undefined) {
        const modelName = stats.model.includes('haiku') ? 'Haiku' : 'Sonnet';
        const costText = `${modelName} • ${stats.input_tokens.toLocaleString()} input + ${stats.output_tokens.toLocaleString()} output tokens • Cost: $${stats.cost.toFixed(4)}`;
        document.getElementById('keywordCostStats').textContent = costText;
    }

    // Render keywords
    keywords.forEach((kw, index) => {
        const item = document.createElement('div');
        item.className = 'asset-item';
        item.dataset.index = index;

        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.checked = true;  // Pre-select all
        checkbox.addEventListener('change', updateKeywordCount);

        const text = document.createElement('span');
        text.className = 'asset-text';
        text.textContent = kw.keyword;

        const metadata = document.createElement('div');
        metadata.className = 'asset-metadata';

        // Match type badge
        const matchBadge = document.createElement('span');
        matchBadge.className = 'asset-badge badge-match-type';
        matchBadge.textContent = kw.match_type;
        metadata.appendChild(matchBadge);

        // Intent badge
        const intentBadge = document.createElement('span');
        intentBadge.className = `asset-badge badge-intent ${kw.intent}`;
        intentBadge.textContent = kw.intent.toUpperCase();
        metadata.appendChild(intentBadge);

        // Search volume badge (if available)
        if (kw.search_volume) {
            const volumeBadge = document.createElement('span');
            volumeBadge.className = 'asset-badge badge-volume';
            volumeBadge.textContent = `${kw.search_volume}/mo`;
            metadata.appendChild(volumeBadge);
        }

        // Relevance score
        const scoreBadge = document.createElement('span');
        scoreBadge.className = 'asset-badge badge-chars';
        scoreBadge.textContent = `${Math.round(kw.relevance_score * 100)}%`;
        if (kw.relevance_score < 0.7) {
            scoreBadge.classList.add('warning');
        }
        metadata.appendChild(scoreBadge);

        item.appendChild(checkbox);
        item.appendChild(text);
        item.appendChild(metadata);

        // Click on item toggles checkbox
        item.addEventListener('click', (e) => {
            if (e.target !== checkbox) {
                checkbox.checked = !checkbox.checked;
                updateKeywordCount();
            }
        });

        list.appendChild(item);
    });

    updateKeywordCount();
}

function updateKeywordCount() {
    const checkboxes = document.querySelectorAll('#keywordList input[type="checkbox"]');
    const selected = Array.from(checkboxes).filter(cb => cb.checked).length;
    document.getElementById('keywordCount').textContent = selected;

    // Update visual selection
    checkboxes.forEach(cb => {
        if (cb.checked) {
            cb.closest('.asset-item').classList.add('selected');
        } else {
            cb.closest('.asset-item').classList.remove('selected');
        }
    });
}

function useSelectedKeywords() {
    const checkboxes = document.querySelectorAll('#keywordList input[type="checkbox"]:checked');
    const keywordList = document.getElementById('keywordList');
    const keywords = [];

    checkboxes.forEach(cb => {
        const item = cb.closest('.asset-item');
        const index = parseInt(item.dataset.index);
        const keywordText = item.querySelector('.asset-text').textContent;
        const matchType = item.querySelector('.badge-match-type').textContent;
        keywords.push(`${keywordText} | ${matchType}`);
    });

    // Populate textarea
    const textarea = document.getElementById('keywords');
    textarea.value = keywords.join('\n');

    closeKeywordModal();
}

function closeKeywordModal() {
    document.getElementById('keywordModal').classList.add('hidden');
}

// =======================
// RSA GENERATION
// =======================

async function handleGenerateRsa() {
    const url = document.getElementById('rsa_final_url').value.trim();
    const client = document.getElementById('client').value;
    const model = document.querySelector('input[name="rsaModel"]:checked').value;

    if (!client) {
        alert('Please select a client first');
        return;
    }

    if (!url) {
        alert('Please enter a final URL');
        return;
    }

    // Open modal
    const modal = document.getElementById('rsaModal');
    modal.classList.remove('hidden');

    // Show loading state
    document.getElementById('rsaLoading').classList.remove('hidden');
    document.getElementById('rsaResults').classList.add('hidden');
    document.getElementById('rsaFooter').classList.add('hidden');

    try {
        const response = await fetch('/api/generate_rsa', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                url: url,
                client: client,
                model: model
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to generate ad copy');
        }

        const data = await response.json();

        // Hide loading, show results
        document.getElementById('rsaLoading').classList.add('hidden');
        document.getElementById('rsaResults').classList.remove('hidden');
        document.getElementById('rsaFooter').classList.remove('hidden');

        // Display results
        displayRsaAssets(data);

    } catch (error) {
        console.error('Error generating RSA:', error);
        alert(`Error: ${error.message}`);
        closeRsaModal();
    }
}

function displayRsaAssets(data) {
    // Display cost stats if available
    if (data.stats && data.stats.cost !== undefined) {
        const modelName = data.stats.model.includes('haiku') ? 'Haiku' : 'Sonnet';
        const costText = `${modelName} • ${data.stats.input_tokens.toLocaleString()} input + ${data.stats.output_tokens.toLocaleString()} output tokens • Cost: $${data.stats.cost.toFixed(4)}`;
        document.getElementById('rsaCostStats').textContent = costText;
    }

    displayAssetList('rsaHeadlineList', data.headlines, 30);
    displayAssetList('rsaDescriptionList', data.descriptions, 90);
}

function displayAssetList(containerId, assets, maxChars) {
    const list = document.getElementById(containerId);
    list.innerHTML = '';

    // Flatten assets (they may be organized by category)
    const flatAssets = [];
    if (assets.benefits) flatAssets.push(...assets.benefits);
    if (assets.features) flatAssets.push(...assets.features);
    if (assets.urgency) flatAssets.push(...assets.urgency);
    if (assets.social_proof) flatAssets.push(...assets.social_proof);

    flatAssets.forEach((text, index) => {
        const item = document.createElement('div');
        item.className = 'asset-item';
        item.dataset.index = index;
        item.dataset.text = text;

        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.checked = true;  // Pre-select all

        const assetText = document.createElement('span');
        assetText.className = 'asset-text';
        assetText.textContent = text;

        const metadata = document.createElement('div');
        metadata.className = 'asset-metadata';

        const charCount = document.createElement('span');
        charCount.className = `asset-badge badge-chars ${text.length > maxChars ? 'warning' : ''}`;
        charCount.textContent = text.length;
        metadata.appendChild(charCount);

        item.appendChild(checkbox);
        item.appendChild(assetText);
        item.appendChild(metadata);

        // Click on item toggles checkbox
        item.addEventListener('click', (e) => {
            if (e.target !== checkbox) {
                checkbox.checked = !checkbox.checked;
                checkbox.checked ? item.classList.add('selected') : item.classList.remove('selected');
            }
        });

        list.appendChild(item);
    });
}

function useSelectedRsa() {
    const headlineCheckboxes = document.querySelectorAll('#rsaHeadlineList input[type="checkbox"]:checked');
    const descriptionCheckboxes = document.querySelectorAll('#rsaDescriptionList input[type="checkbox"]:checked');

    const headlines = Array.from(headlineCheckboxes).map(cb =>
        cb.closest('.asset-item').dataset.text
    );

    const descriptions = Array.from(descriptionCheckboxes).map(cb =>
        cb.closest('.asset-item').dataset.text
    );

    // Populate textareas
    document.getElementById('rsa_headlines').value = headlines.join('\n');
    document.getElementById('rsa_descriptions').value = descriptions.join('\n');

    closeRsaModal();
}

function closeRsaModal() {
    document.getElementById('rsaModal').classList.add('hidden');
}

// =======================
// ASSET GROUP GENERATION
// =======================

async function handleGenerateAssetGroup() {
    const url = document.getElementById('final_urls').value.trim();
    const client = document.getElementById('client').value;
    const model = document.querySelector('input[name="assetGroupModel"]:checked').value;

    if (!client) {
        alert('Please select a client first');
        return;
    }

    if (!url) {
        alert('Please enter a final URL');
        return;
    }

    // Open modal
    const modal = document.getElementById('assetGroupModal');
    modal.classList.remove('hidden');

    // Show loading state
    document.getElementById('assetGroupLoading').classList.remove('hidden');
    document.getElementById('assetGroupResults').classList.add('hidden');
    document.getElementById('assetGroupFooter').classList.add('hidden');

    try {
        const response = await fetch('/api/generate_asset_group', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                url: url,
                model: model,
                client: client
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to generate asset group assets');
        }

        const data = await response.json();

        // Hide loading, show results
        document.getElementById('assetGroupLoading').classList.add('hidden');
        document.getElementById('assetGroupResults').classList.remove('hidden');
        document.getElementById('assetGroupFooter').classList.remove('hidden');

        // Display results
        displayAssetGroupAssets(data);

    } catch (error) {
        console.error('Error generating asset group:', error);
        alert(`Error: ${error.message}`);
        closeAssetGroupModal();
    }
}

function displayAssetGroupAssets(data) {
    // Display cost stats if available
    if (data.stats && data.stats.cost !== undefined) {
        const modelName = data.stats.model.includes('haiku') ? 'Haiku' : 'Sonnet';
        const costText = `${modelName} • ${data.stats.input_tokens.toLocaleString()} input + ${data.stats.output_tokens.toLocaleString()} output tokens • Cost: $${data.stats.cost.toFixed(4)}`;
        document.getElementById('assetGroupCostStats').textContent = costText;
    }

    displayAssetList('shortHeadlineList', data.short_headlines, 30);
    displayAssetList('longHeadlineList', data.long_headlines, 90);
    displayAssetList('assetGroupDescriptionList', data.descriptions, 90);
}

function useSelectedAssetGroup() {
    const shortHeadlineCheckboxes = document.querySelectorAll('#shortHeadlineList input[type="checkbox"]:checked');
    const longHeadlineCheckboxes = document.querySelectorAll('#longHeadlineList input[type="checkbox"]:checked');
    const descriptionCheckboxes = document.querySelectorAll('#assetGroupDescriptionList input[type="checkbox"]:checked');

    const shortHeadlines = Array.from(shortHeadlineCheckboxes).map(cb =>
        cb.closest('.asset-item').dataset.text
    );

    const longHeadlines = Array.from(longHeadlineCheckboxes).map(cb =>
        cb.closest('.asset-item').dataset.text
    );

    const descriptions = Array.from(descriptionCheckboxes).map(cb =>
        cb.closest('.asset-item').dataset.text
    );

    // Populate textareas
    document.getElementById('headlines').value = shortHeadlines.join('\n');
    document.getElementById('long_headlines').value = longHeadlines.join('\n');
    document.getElementById('descriptions').value = descriptions.join('\n');

    closeAssetGroupModal();
}

function closeAssetGroupModal() {
    document.getElementById('assetGroupModal').classList.add('hidden');
}
