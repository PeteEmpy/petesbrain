// Google Ads Campaign Builder - Progressive Disclosure Logic

document.addEventListener('DOMContentLoaded', function() {
    // Form elements
    const clientSelect = document.getElementById('client');
    const campaignTypeRadios = document.querySelectorAll('input[name="campaign_type"]');
    const actionRadios = document.querySelectorAll('input[name="action"]');
    const createTypeRadios = document.querySelectorAll('input[name="create_type"]');
    const biddingStrategyRadios = document.querySelectorAll('input[name="bidding_strategy"]');
    const form = document.getElementById('campaignForm');

    // Form sections
    const step2 = document.getElementById('step2');
    const step3 = document.getElementById('step3');
    const step4a = document.getElementById('step4a');
    const step4b_campaign = document.getElementById('step4b_campaign');
    const step4b_adgroup = document.getElementById('step4b_adgroup');
    const step4b_assetgroup = document.getElementById('step4b_assetgroup');
    const step5_adgroup_additions = document.getElementById('step5_adgroup_additions');
    const step5_campaign_additions = document.getElementById('step5_campaign_additions');
    const step5_assetgroup_additions = document.getElementById('step5_assetgroup_additions');
    const step6a_keywords = document.getElementById('step6a_keywords');
    const step6b_rsas = document.getElementById('step6b_rsas');
    const step6c_sitelinks = document.getElementById('step6c_sitelinks');
    const step6d_callouts = document.getElementById('step6d_callouts');
    const submitSection = document.getElementById('submitSection');

    // State tracking
    let currentClient = null;
    let currentCampaignType = null;
    let currentAction = null;
    let campaigns = [];

    // Step 1: Client selection
    clientSelect.addEventListener('change', function() {
        currentClient = this.value;

        if (currentClient) {
            // Show step 2
            step2.classList.remove('hidden');
            // Reset subsequent steps
            resetFromStep(3);
        } else {
            resetFromStep(2);
        }
    });

    // Step 2: Campaign type selection
    campaignTypeRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            currentCampaignType = this.value;

            // Update label for existing campaign option
            const label = document.getElementById('existingCampaignLabel');
            if (currentCampaignType === 'PERFORMANCE_MAX') {
                label.textContent = 'Add to Existing Performance Max Campaign';
            } else {
                label.textContent = 'Add to Existing Search Campaign';
            }

            // Show step 3
            step3.classList.remove('hidden');
            // Reset subsequent steps
            resetFromStep(4);
        });
    });

    // Step 3: New or existing campaign
    actionRadios.forEach(radio => {
        radio.addEventListener('change', async function() {
            currentAction = this.value;

            if (currentAction === 'new_campaign') {
                // Show campaign creation form
                step4a.classList.add('hidden');
                step4b_campaign.classList.remove('hidden');
                step4b_adgroup.classList.add('hidden');
                step4b_assetgroup.classList.add('hidden');
                step5_campaign_additions.classList.remove('hidden');
                step5_adgroup_additions.classList.add('hidden');
                step5_assetgroup_additions.classList.add('hidden');
                submitSection.style.display = 'block';
            } else if (currentAction === 'existing_campaign') {
                // Load existing campaigns
                await loadCampaigns();
                step4a.classList.remove('hidden');
                step4b_campaign.classList.add('hidden');
                step4b_adgroup.classList.add('hidden');
                step4b_assetgroup.classList.add('hidden');
                step5_campaign_additions.classList.add('hidden');
                step5_adgroup_additions.classList.add('hidden');
                step5_assetgroup_additions.classList.add('hidden');
                submitSection.style.display = 'none';
            }
        });
    });

    // Step 4a: What to create in existing campaign
    createTypeRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            const createType = this.value;

            if (createType === 'ad_group') {
                step4b_adgroup.classList.remove('hidden');
                step4b_assetgroup.classList.add('hidden');
                step5_adgroup_additions.classList.remove('hidden');
                step5_assetgroup_additions.classList.add('hidden');
                step6a_keywords.classList.add('hidden');
                step6b_rsas.classList.add('hidden');
                step6c_sitelinks.classList.add('hidden');
                step6d_callouts.classList.add('hidden');
                submitSection.style.display = 'block';
            } else if (createType === 'asset_group') {
                step4b_adgroup.classList.add('hidden');
                step4b_assetgroup.classList.remove('hidden');
                step5_adgroup_additions.classList.add('hidden');
                step5_assetgroup_additions.classList.remove('hidden');
                step6a_keywords.classList.add('hidden');
                step6b_rsas.classList.add('hidden');
                step6c_sitelinks.classList.add('hidden');
                step6d_callouts.classList.add('hidden');
                submitSection.style.display = 'block';
            }
        });
    });

    // Step 5: Checkboxes for what to add

    // Ad Group additions
    const addKeywordsCheckbox = document.getElementById('add_keywords');
    const addRsasCheckbox = document.getElementById('add_rsas');
    const addSitelinksAdGroupCheckbox = document.getElementById('add_sitelinks_adgroup');
    const addCalloutsAdGroupCheckbox = document.getElementById('add_callouts_adgroup');

    // Campaign additions
    const addSitelinksCampaignCheckbox = document.getElementById('add_sitelinks_campaign');
    const addCalloutsCampaignCheckbox = document.getElementById('add_callouts_campaign');

    // Asset Group additions
    const addSitelinksAssetGroupCheckbox = document.getElementById('add_sitelinks_assetgroup');
    const addCalloutsAssetGroupCheckbox = document.getElementById('add_callouts_assetgroup');

    // Keywords checkbox
    if (addKeywordsCheckbox) {
        addKeywordsCheckbox.addEventListener('change', function() {
            if (this.checked) {
                step6a_keywords.classList.remove('hidden');
            } else {
                step6a_keywords.classList.add('hidden');
            }
        });
    }

    // RSAs checkbox
    if (addRsasCheckbox) {
        addRsasCheckbox.addEventListener('change', function() {
            if (this.checked) {
                step6b_rsas.classList.remove('hidden');
            } else {
                step6b_rsas.classList.add('hidden');
            }
        });
    }

    // Sitelinks checkboxes (all three contexts)
    if (addSitelinksAdGroupCheckbox) {
        addSitelinksAdGroupCheckbox.addEventListener('change', function() {
            if (this.checked) {
                step6c_sitelinks.classList.remove('hidden');
            } else {
                step6c_sitelinks.classList.add('hidden');
            }
        });
    }

    if (addSitelinksCampaignCheckbox) {
        addSitelinksCampaignCheckbox.addEventListener('change', function() {
            if (this.checked) {
                step6c_sitelinks.classList.remove('hidden');
            } else {
                step6c_sitelinks.classList.add('hidden');
            }
        });
    }

    if (addSitelinksAssetGroupCheckbox) {
        addSitelinksAssetGroupCheckbox.addEventListener('change', function() {
            if (this.checked) {
                step6c_sitelinks.classList.remove('hidden');
            } else {
                step6c_sitelinks.classList.add('hidden');
            }
        });
    }

    // Callouts checkboxes (all three contexts)
    if (addCalloutsAdGroupCheckbox) {
        addCalloutsAdGroupCheckbox.addEventListener('change', function() {
            if (this.checked) {
                step6d_callouts.classList.remove('hidden');
            } else {
                step6d_callouts.classList.add('hidden');
            }
        });
    }

    if (addCalloutsCampaignCheckbox) {
        addCalloutsCampaignCheckbox.addEventListener('change', function() {
            if (this.checked) {
                step6d_callouts.classList.remove('hidden');
            } else {
                step6d_callouts.classList.add('hidden');
            }
        });
    }

    if (addCalloutsAssetGroupCheckbox) {
        addCalloutsAssetGroupCheckbox.addEventListener('change', function() {
            if (this.checked) {
                step6d_callouts.classList.remove('hidden');
            } else {
                step6d_callouts.classList.add('hidden');
            }
        });
    }

    // Bidding strategy toggle (for new campaigns)
    biddingStrategyRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            const targetRoasField = document.getElementById('target_roas_field');
            const targetCpaField = document.getElementById('target_cpa_field');

            if (this.value === 'target_roas') {
                targetRoasField.classList.remove('hidden');
                targetCpaField.classList.add('hidden');
            } else {
                targetRoasField.classList.add('hidden');
                targetCpaField.classList.remove('hidden');
            }
        });
    });

    // Hide/show asset group option based on campaign type
    campaignTypeRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            const assetGroupOption = document.getElementById('option_asset_group');
            if (this.value === 'PERFORMANCE_MAX') {
                assetGroupOption.style.display = 'flex';
            } else {
                assetGroupOption.style.display = 'none';
                // If asset group was selected, deselect it
                const assetGroupRadio = document.querySelector('input[value="asset_group"]');
                if (assetGroupRadio && assetGroupRadio.checked) {
                    assetGroupRadio.checked = false;
                }
            }
        });
    });

    // Load campaigns from backend
    async function loadCampaigns() {
        const select = document.getElementById('existing_campaign');
        select.innerHTML = '<option value="">-- Loading campaigns... --</option>';
        select.disabled = true;

        try {
            const response = await fetch('/api/get_campaigns', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    client: currentClient,
                    campaign_type: currentCampaignType
                })
            });

            if (!response.ok) {
                throw new Error('Failed to load campaigns');
            }

            const data = await response.json();
            campaigns = data.campaigns;

            // Populate dropdown
            select.innerHTML = '<option value="">-- Select Campaign --</option>';
            campaigns.forEach(campaign => {
                const option = document.createElement('option');
                option.value = campaign.id;
                option.textContent = campaign.name;
                select.appendChild(option);
            });

            select.disabled = false;

        } catch (error) {
            console.error('Error loading campaigns:', error);
            select.innerHTML = '<option value="">-- Error loading campaigns --</option>';
        }
    }

    // Form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Validate and gather form data
        const formData = gatherFormData();

        if (!formData) {
            alert('Please fill in all required fields');
            return;
        }

        // Submit to backend
        await submitForm(formData);
    });

    function gatherFormData() {
        const data = {
            client: currentClient,
            action: null,
            campaign_data: null,
            ad_group_data: null,
            asset_group_data: null,
            campaign_id: null
        };

        if (currentAction === 'new_campaign') {
            // New campaign
            data.action = 'new_campaign';

            const campaignName = document.getElementById('campaign_name').value;
            const dailyBudget = parseFloat(document.getElementById('daily_budget').value);
            const biddingStrategy = document.querySelector('input[name="bidding_strategy"]:checked')?.value;
            const locations = document.getElementById('locations').value;

            if (!campaignName || !dailyBudget || !biddingStrategy) {
                return null;
            }

            data.campaign_data = {
                campaign_name: campaignName,
                daily_budget_micros: Math.round(dailyBudget * 1000000), // Convert £ to micros
                campaign_type: currentCampaignType,
                locations: [locations],
                status: 'PAUSED'  // ALWAYS PAUSED
            };

            if (biddingStrategy === 'target_roas') {
                const targetRoas = parseFloat(document.getElementById('target_roas').value);
                if (!targetRoas) return null;
                data.campaign_data.target_roas = targetRoas / 100; // Convert % to decimal
            } else {
                const targetCpa = parseFloat(document.getElementById('target_cpa').value);
                if (!targetCpa) return null;
                data.campaign_data.target_cpa_micros = Math.round(targetCpa * 1000000);
            }

        } else {
            // Existing campaign
            const campaignId = document.getElementById('existing_campaign').value;
            if (!campaignId) return null;

            data.campaign_id = campaignId;

            const createType = document.querySelector('input[name="create_type"]:checked')?.value;
            if (!createType) return null;

            if (createType === 'ad_group') {
                // New ad group
                data.action = 'new_ad_group';

                const adGroupName = document.getElementById('ad_group_name').value;
                if (!adGroupName) return null;

                data.ad_group_data = {
                    ad_group_name: adGroupName,
                    status: 'PAUSED'  // ALWAYS PAUSED
                };

                const cpcBid = document.getElementById('cpc_bid').value;
                if (cpcBid) {
                    data.ad_group_data.cpc_bid_micros = Math.round(parseFloat(cpcBid) * 1000000);
                }

            } else {
                // New asset group
                data.action = 'new_asset_group';

                const assetGroupName = document.getElementById('asset_group_name').value;
                const finalUrls = document.getElementById('final_urls').value;
                const businessName = document.getElementById('business_name').value;
                const headlinesText = document.getElementById('headlines').value;
                const longHeadlinesText = document.getElementById('long_headlines').value;
                const descriptionsText = document.getElementById('descriptions').value;

                if (!assetGroupName || !finalUrls || !businessName || !headlinesText || !longHeadlinesText || !descriptionsText) {
                    return null;
                }

                // Split text areas into arrays
                const headlines = headlinesText.split('\n').filter(h => h.trim()).map(h => h.trim());
                const longHeadlines = longHeadlinesText.split('\n').filter(h => h.trim()).map(h => h.trim());
                const descriptions = descriptionsText.split('\n').filter(d => d.trim()).map(d => d.trim());

                // Validate counts
                if (headlines.length < 3 || headlines.length > 5) {
                    alert('Please provide 3-5 headlines');
                    return null;
                }
                if (longHeadlines.length < 1 || longHeadlines.length > 5) {
                    alert('Please provide 1-5 long headlines');
                    return null;
                }
                if (descriptions.length < 2 || descriptions.length > 5) {
                    alert('Please provide 2-5 descriptions');
                    return null;
                }

                data.asset_group_data = {
                    asset_group_name: assetGroupName,
                    final_urls: [finalUrls],
                    business_name: businessName,
                    headlines: headlines,
                    long_headlines: longHeadlines,
                    descriptions: descriptions,
                    status: 'PAUSED'  // ALWAYS PAUSED
                };
            }
        }

        return data;
    }

    async function submitForm(formData) {
        const submitBtn = document.getElementById('submitBtn');
        submitBtn.disabled = true;
        submitBtn.textContent = 'Creating...';

        try {
            const response = await fetch('/api/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            if (response.ok) {
                showSuccess(result);
            } else {
                showError(result.error || 'Unknown error occurred');
            }

        } catch (error) {
            console.error('Error submitting form:', error);
            showError(error.message);
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Create (PAUSED State)';
        }
    }

    function showSuccess(result) {
        const resultDiv = document.getElementById('result');
        const resultContent = document.getElementById('resultContent');

        let message = `<p><strong>${result.message}</strong></p>`;

        if (result.campaign_id) {
            message += `<p>Campaign ID: <code>${result.campaign_id}</code></p>`;
        }
        if (result.ad_group_id) {
            message += `<p>Ad Group ID: <code>${result.ad_group_id}</code></p>`;
        }
        if (result.asset_group_id) {
            message += `<p>Asset Group ID: <code>${result.asset_group_id}</code></p>`;
        }

        message += `<p class="alert alert-warning"><strong>⚠️ Created in PAUSED state.</strong> Review in Google Ads before enabling.</p>`;

        resultContent.innerHTML = message;
        resultDiv.classList.remove('hidden');
        form.classList.add('hidden');
    }

    function showError(errorMessage) {
        const errorDiv = document.getElementById('error');
        const errorContent = document.getElementById('errorContent');

        errorContent.innerHTML = `<p>${errorMessage}</p>`;
        errorDiv.classList.remove('hidden');
    }

    function resetFromStep(stepNumber) {
        const steps = [step2, step3, step4a, step4b_campaign, step4b_adgroup, step4b_assetgroup,
                       step5_adgroup_additions, step5_campaign_additions, step5_assetgroup_additions,
                       step6a_keywords, step6b_rsas, step6c_sitelinks, step6d_callouts];

        for (let i = stepNumber - 2; i < steps.length; i++) {
            if (steps[i]) {
                steps[i].classList.add('hidden');
            }
        }

        submitSection.style.display = 'none';

        // Reset radios and checkboxes
        if (stepNumber <= 2) {
            campaignTypeRadios.forEach(r => r.checked = false);
            currentCampaignType = null;
        }
        if (stepNumber <= 3) {
            actionRadios.forEach(r => r.checked = false);
            currentAction = null;
        }
        if (stepNumber <= 4) {
            createTypeRadios.forEach(r => r.checked = false);
            biddingStrategyRadios.forEach(r => r.checked = false);
        }
        if (stepNumber <= 5) {
            // Reset all checkboxes
            if (addKeywordsCheckbox) addKeywordsCheckbox.checked = false;
            if (addRsasCheckbox) addRsasCheckbox.checked = false;
            if (addSitelinksAdGroupCheckbox) addSitelinksAdGroupCheckbox.checked = false;
            if (addCalloutsAdGroupCheckbox) addCalloutsAdGroupCheckbox.checked = false;
            if (addSitelinksCampaignCheckbox) addSitelinksCampaignCheckbox.checked = false;
            if (addCalloutsCampaignCheckbox) addCalloutsCampaignCheckbox.checked = false;
            if (addSitelinksAssetGroupCheckbox) addSitelinksAssetGroupCheckbox.checked = false;
            if (addCalloutsAssetGroupCheckbox) addCalloutsAssetGroupCheckbox.checked = false;
        }
    }
});
