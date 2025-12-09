import app.services.gemini as gemini_module


def test_mock_gemini(mocker):
 
    fake_result = {
        "summary": "Résumé simulé",
        "tone": "positif",
        "category": "Sport",
        "score": 0.92
    }

    def fake_gemini(text):
        return fake_result

  
    mocker.patch.object(
        gemini_module,
        "summarize_and_analyze_tone",
        side_effect=fake_gemini
    )

   
    result = gemini_module.summarize_and_analyze_tone("Texte test")

    assert isinstance(result, dict)
    assert result["summary"] == "Résumé simulé"
    assert result["tone"] == "positif"
    assert result["category"] == "Sport"
    assert result["score"] == 0.92
