#!/usr/bin/env ruby
require 'json'
require_relative 'anagram_client'
require 'minitest/autorun'
#require 'test/unit'

# capture ARGV before TestUnit Autorunner clobbers it

#class TestCases < Test::Unit::TestCase
class TestCases < Minitest::Test
  # runs before each test
  def setup
    @client = AnagramClient.new(ARGV)

    # add words to the dictionary
    @client.post('/words.json', nil, {"words" => ["read", "dear", "dare"] }) rescue nil
  end

  # runs after each test
  def teardown
    # delete everything
    @client.delete('/words.json') rescue nil
  end

  def test_adding_words
    res = @client.post('/words.json', nil, {"words" => ["read", "dear", "dare"] })
    assert_equal('201', res.code, "Unexpected response code")
  end

  # Robert Crimi
  def test_adding_words_twice
    res = @client.post('/words.json', nil, {"words" => ["read", "dear", "dare"] })
    assert_equal('201', res.code, "Unexpected response code")
    res = @client.post('/words.json', nil, {"words" => ["read", "dear", "dare"] })
    assert_equal('201', res.code, "Unexpected response code")
    
    # fetch anagrams
    res = @client.get('/anagrams/read.json')
    assert_equal('200', res.code, "Unexpected response code")
    assert res.body != nil

    body = JSON.parse(res.body)
    assert body['anagrams'] != nil

    expected_anagrams = %w(dare dear)
    assert_equal(expected_anagrams, body['anagrams'].sort)
  end

  def test_fetching_anagrams

    # fetch anagrams
    res = @client.get('/anagrams/read.json')
    assert_equal('200', res.code, "Unexpected response code")
    assert res.body != nil

    body = JSON.parse(res.body)
    assert body['anagrams'] != nil

    expected_anagrams = %w(dare dear)
    assert_equal(expected_anagrams, body['anagrams'].sort)
  end

  def test_fetching_anagrams_with_limit

    # fetch anagrams with limit
    res = @client.get('/anagrams/read.json', 'limit=1')
    assert_equal('200', res.code, "Unexpected response code")

    body = JSON.parse(res.body)
    assert_equal(1, body['anagrams'].size)
  end

  def test_fetch_for_word_with_no_anagrams

    # fetch anagrams with limit
    res = @client.get('/anagrams/zyxwv.json')
    assert_equal('200', res.code, "Unexpected response code")

    body = JSON.parse(res.body)
    assert_equal(0, body['anagrams'].size)
  end

  def test_deleting_all_words

    res = @client.delete('/words.json')
    assert_equal('204', res.code, "Unexpected response code")

    # should fetch an empty body
    res = @client.get('/anagrams/read.json')
    assert_equal('200', res.code, "Unexpected response code")

    body = JSON.parse(res.body)
    assert_equal(0, body['anagrams'].size)
  end

  def test_deleting_all_words_multiple_times

    3.times do
      res = @client.delete('/words.json')
      assert_equal('204', res.code, "Unexpected response code")
    end

    # should fetch an empty body
    res = @client.get('/anagrams/read.json', 'limit=1')
    assert_equal('200', res.code, "Unexpected response code")

    body = JSON.parse(res.body)
    assert_equal(0, body['anagrams'].size)
  end

  def test_deleting_single_word

    # delete the word
    res = @client.delete('/words/dear.json')
    assert_equal('200', res.code, "Unexpected response code")

    # expect it not to show up in results
    res = @client.get('/anagrams/read.json')
    assert_equal('200', res.code, "Unexpected response code")

    body = JSON.parse(res.body)
    assert_equal(['dare'], body['anagrams'])
  end

  # Robert Crimi
  def test_deleting_word_not_in_corpus
    res = @client.delete('/words/foo.json')
    assert_equal('200', res.code, "Unexpected response code")

    body = JSON.parse(res.body)
    assert_equal("(foo) not in corpus", body["Response"])
  end

  # Robert Crimi
  def test_word_count
    res = @client.post('/words.json', nil, {"words" => ["foo", "bar"] })
    assert_equal('201', res.code, "Unexpected response code")
    
    res = @client.get('/wordCount.json')
    assert_equal('200', res.code, "Unexpected response code")

    body = JSON.parse(res.body)
    assert_equal(5, body['wordCount'])
    assert_equal(3, body['minLen'])
    assert_equal(4, body['maxLen'])
    assert_equal(4, body['medianLen'])
    assert_equal(3.6, body['averageLen'])
  end

  # Robert Crimi
  def test_word_count_no_words_in_corpus
    res = @client.delete('/words.json')
    assert_equal('204', res.code, "Unexpected response code")

    res = @client.get('/wordCount.json')
    assert_equal('200', res.code, "Unexpected response code")

    body = JSON.parse(res.body)
    assert_equal('No words in the corpus', body['Response'])
  end

  # Robert Crimi
  def test_proper_noun_false
    res = @client.post('/words.json', nil, {"words" => ["Foo", "oof", "ofo"] })
    assert_equal('201', res.code, "Unexpected response code")

    res = @client.get('/anagrams/oof.json', 'includeProper=False')
    assert_equal('200', res.code, "Unexpected response code")

    body = JSON.parse(res.body)
    expected_anagrams = %w(ofo)
    assert_equal(expected_anagrams, body['anagrams'].sort)
  end

  # Robert Crimi
  def test_proper_noun_false_and_limit
    res = @client.post('/words.json', nil, {"words" => ["Foo", "oof", "ofo", "foo"] })
    assert_equal('201', res.code, "Unexpected response code")

    res = @client.get('/anagrams/oof.json', 'includeProper=False&limit=1')
    assert_equal('200', res.code, "Unexpected response code")

    body = JSON.parse(res.body)
    assert_equal(1, body['anagrams'].size)
    expected_anagrams = %w(ofo)
    assert_equal(expected_anagrams, body['anagrams'].sort)  
  end

  # Robert Crimi
  def test_most_anagrams
    res = @client.post('/words.json', nil, {"words" => ["foo", "oof"] })
    assert_equal('201', res.code, "Unexpected response code")

    res = @client.get('/mostAnagrams.json')
    assert_equal('200', res.code, "Unexpected response code")

    body = JSON.parse(res.body)
    expected_anagrams = %w(read dear dare)
    assert_equal(expected_anagrams, body['Most Anagrams'])    
  end

  # Robert Crimi
  def test_most_anagrams_no_words_in_corpus
    res = @client.delete('/words.json')
    assert_equal('204', res.code, "Unexpected response code")

    res = @client.get('/mostAnagrams.json')
    assert_equal('200', res.code, "Unexpected response code")

    body = JSON.parse(res.body)
    assert_equal("No words in the corpus", body['Most Anagrams'])    
  end

  # Robert Crimi
  def test_all_anagrams_true
    res = @client.post('/allAnagrams.json', nil, {"words" => ["read", "dear", "dare"]})
    assert_equal('200', res.code, "Unexpected response code")
    
    body = JSON.parse(res.body)
    assert_equal(true, body['All Anagrams'])  
  end

  # Robert Crimi
  def test_all_anagrams_false
    res = @client.post('/allAnagrams.json', nil, {"words" => ["read", "dear", "foo"]})
    assert_equal('200', res.code, "Unexpected response code")
    
    body = JSON.parse(res.body)
    assert_equal(false, body['All Anagrams'])  
  end

  # Robert Crimi
  def test_delete_anagram_groups_of_size
    res = @client.post('/words.json', nil, {"words" => ["foo", "oof"] })
    assert_equal('201', res.code, "Unexpected response code")

    res = @client.delete('/deleteAllGroups/3.json')
    assert_equal('204', res.code, "Unexpected response code")

    res = @client.get('/wordCount.json')
    assert_equal('200', res.code, "Unexpected response code")

    body = JSON.parse(res.body)
    assert_equal(2, body['wordCount'])
    assert_equal(3, body['minLen'])
    assert_equal(3, body['maxLen'])
    assert_equal(3, body['medianLen'])
    assert_equal(3, body['averageLen'])
  end

  # Robert Crimi
  def test_delete_all_anagrams_of_word
    res = @client.delete('/deleteAllAnagrams/read.json')
    assert_equal('204', res.code, "Unexpected response code")

    res = @client.get('/wordCount.json')
    assert_equal('200', res.code, "Unexpected response code")

    body = JSON.parse(res.body)
    assert_equal("No words in the corpus", body['Response'])
  end
end








