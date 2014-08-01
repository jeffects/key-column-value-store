require './key_column_value_store'
require 'debugger'
describe KeyColumnValueStore do

  let(:store) { KeyColumnValueStore.new }

  describe '#set' do
    it 'sets the correct value' do
      store.set('a', 'aa', 'x')
      store.get('a', 'aa').should eq('x')
    end
  end

  describe '#get' do
    it 'retrieves the correct value' do
      store.set('a', 'aa', 'x')
      store.set('a', 'ab', 'x2')
      store.set('d', 'de', 'xd')
      store.set('d', 'df', 'xd')
      expect(store.get('a', 'aa')).to eq 'x'
    end

    it 'returns nil for nonexistent columns' do
      expect(store.get('o', 'o')).to eq nil
    end
  end

  describe '#get_key' do
    it "sets different values on the 'a' key" do
      store.set('a', 'aa', 'y')
      store.set('a', 'ab', 'z')
      expect(store.get_key('a')).to eq([['aa', 'y'], ['ab', 'z']])
    end

    context 'store is empty' do
      it 'returns empty array' do
        expect(store.get_key('a')).to eq []
      end
    end
  end

  describe '#get_keys' do
    it "returns 'a' and 'z'" do
      store.set('a', 'aa', 'x')
      store.set('z', 'bb', 'y')
      expect(store.get_keys).to eq ['a', 'z']
    end

    context 'key does not exist in store' do
      it 'returns nil if key does not exist' do
        store.set('a', 'aa', 'x')
        expect(store.get('b', 'bb')).to eq nil
      end
    end

    context 'column does not exist in store' do
      it 'returns nil' do
        store.set('a', 'aa', 'x')
        expect(store.get('a', 'bb')).to eq nil
      end
    end
  end

  describe '#delete' do
    it 'removes a column/value from a given array' do
      store.set('a', 'aa', 'x')
      store.set('z', 'bb', 'y')
      store.delete('a', 'aa')
      expect(store.get_key('a')).to eq []
      expect(store.get_keys).to eq ['a', 'z']
    end

    context 'empty store' do
      it 'returns empty array' do
        expect(store.delete('a', 'aa')).to eq []
      end
    end

    context 'non-existent column' do
      it 'returns nil' do
        store.set('a', 'aa', 'x')
        store.delete('a', 'bb')
        expect(store.get('a', 'bb')).to eq nil
        expect(store.get('a', 'aa')).to eq 'x'
      end
    end
  end

  describe '#delete_key' do
    it 'removes all data associated with the given key' do
      store.set('a', 'aa', 'x')
      store.set('a', 'bb', 'y')
      store.set('b', 'aa', 'x')
      store.delete_key('a')
      store.get('a', 'aa').should eq nil
      store.get_key('a').should eq []
    end

    context 'empty store' do
      it 'returns []' do
        expect(store.delete_key('a')).to eq []
      end
    end
  end

  describe '#get_slice' do
    it 'returns true' do
      store.set('a', 'aa', 'x')
      store.set('a', 'ab', 'x')
      store.set('a', 'ac', 'x')
      store.set('a', 'ad', 'x')
      store.set('a', 'ae', 'x')
      store.set('a', 'af', 'x')
      store.set('a', 'ag', 'x')
      expect(store.get_slice('a', 'ac', 'ae')).to eq([['ac', 'x'], ['ad', 'x'], ['ae', 'x']])
      expect(store.get_slice('a', 'ae', nil)).to eq([['ae', 'x'], ['af', 'x'], ['ag', 'x']])
      expect(store.get_slice('a', nil, 'ac')).to eq([['aa', 'x'], ['ab', 'x'], ['ac', 'x']])
    end
  end

end
