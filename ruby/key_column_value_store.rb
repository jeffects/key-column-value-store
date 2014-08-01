class KeyColumnValueStore

  def initialize
    @store = Hash.new
  end

  def set(key, col, val)
    if @store[key].nil?
      @store[key] = {col => val}
    else
      @store[key][col] = val
    end
  end

  def get(key, col)
    if @store[key].nil?
      nil
    else
      @store[key][col]
    end
  end

  # returns empty array if nil
  def get_key(key)
    result = []
    return result if @store[key].nil?
    @store[key].each do |k, v|
      result << [k, v]
    end
    result
  end

  # returns a set containing all of the keys in the store
  def get_keys
    @store.keys
  end

  # removes a column/value from the given key
  def delete(key, col)
    return [] if @store[key].nil?
    @store[key].delete(col)
  end

  def delete_key(key)
    return [] if @store[key].nil?
    @store.delete(key)
  end


  # returns a sorted list of column/value tuples where the column
  # values are between the start and stop values, inclusive of the
  # start and stop values. Start and/or stop can be None values,
  # leaving the slice open ended in that direction
  def get_slice(key, start=nil, stop=nil)
    return [] if @store[key].nil?
    arr = @store[key].sort
    start_index = get_start_index(arr, start)
    stop_index = get_stop_index(arr, start_index, stop)
    arr[start_index..stop_index]
  end

  private
  def get_start_index(arr, column_to_start)
    return 0 if column_to_start.nil?
    arr.index { |a| a.first == column_to_start }
  end

  def get_stop_index(arr, start_index, column_to_stop)
    if column_to_stop.nil?
      start_index + 2
    else
      arr.index { |a| a.first == column_to_stop }
    end
  end

end
